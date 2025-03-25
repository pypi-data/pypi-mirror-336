import argparse
import logging
import sys
from argparse import ArgumentParser, BooleanOptionalAction
from datetime import datetime
from os import listdir
from os.path import join, isfile, splitext, basename, isdir
from pathlib import Path

from indiquo.core.CandidatePredictorDummy import CandidatePredictorDummy
from indiquo.core.CandidatePredictorSum import CandidatePredictorSum
from indiquo.core.IndiQuoBase import IndiQuoBase
from indiquo.core.IndiQuoException import IndiQuoException
from indiquo.core.IndiQuoSum import IndiQuoSum
from indiquo.core.ScenePredictorDummy import ScenePredictorDummy
from indiquo.training.scene import TrainSceneIdentification

try:
    from flair.models import SequenceTagger
    from indiquo.core.CandidatePredictorRW import CandidatePredictorRW
except ModuleNotFoundError:
    pass

from dramatist.core.Dramatist import Dramatist
from indiquo.core.CandidatePredictorST import CandidatePredictorST
from indiquo.core.IndiQuo import IndiQuo
from indiquo.core.ScenePredictor import ScenePredictor
from indiquo.core.chunker.SentenceChunker import SentenceChunker
from indiquo.core.CandidatePredictor import CandidatePredictor
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import csv
from indiquo.training.candidate import TrainCandidateClassifier, TrainCandidateClassifierST


logger = logging.getLogger(__name__)


def __train_candidate(train_folder_path: str, output_folder_path: str, model_name: str):
    TrainCandidateClassifier.train(train_folder_path, output_folder_path, model_name)


def __train_candidate_st(train_folder_path: str, output_folder_path: str, model_name: str):
    TrainCandidateClassifierST.train(train_folder_path, output_folder_path, model_name)


def __train_scene(train_folder_path: str, output_folder_path: str, model_name: str):
    TrainSceneIdentification.train(train_folder_path, output_folder_path, model_name)


def __process_file(indi_quo: IndiQuoBase, filename: str, target_text: str, output_folder_path: str):
    logger.info(f'Processing {filename} ...')

    matches = indi_quo.compare(target_text)

    with open(join(output_folder_path, f'{filename}.tsv'), 'w', encoding='utf-8') as output_file:
        writer = csv.writer(output_file, delimiter='\t', lineterminator='\n')
        writer.writerow(['start', 'end', 'text', 'score', 'scenes'])

        for m in matches:
            scene_predictions = ''

            for sp in m.scene_predictions:
                if scene_predictions:
                    scene_predictions += '#'

                scene_predictions += f'{sp.act}:{sp.scene}:{sp.score}'

            speech_text = m.target_text.replace('\n', ' ')
            writer.writerow([m.target_start, m.target_end, speech_text, m.score, scene_predictions])


def __run_compare(compare_approach: str, model_type: str, source_file_path: str, target_path: str,
                  candidate_model_path: str, scene_model_path: str, output_folder_path: str, add_context: bool,
                  max_candidate_length: int, summaries_file_path: str):
    drama_processor = Dramatist()
    drama = drama_processor.from_file(source_file_path)
    sentence_chunker = SentenceChunker(min_length=10, max_length=64, max_sentences=1)

    if compare_approach == 'candidate':
        if model_type == 'iq':
            candidate_tokenizer = AutoTokenizer.from_pretrained(candidate_model_path)
            candidate_model = AutoModelForSequenceClassification.from_pretrained(candidate_model_path)
            candidate_predictor = CandidatePredictor(candidate_tokenizer, candidate_model, sentence_chunker,
                                                     add_context, max_candidate_length)
        elif model_type == 'st':
            candidate_model = SentenceTransformer(candidate_model_path)
            candidate_predictor = CandidatePredictorST(drama, candidate_model, sentence_chunker, add_context,
                                                       max_candidate_length)
        elif model_type == 'rw':
            candidate_model = SequenceTagger.load(candidate_model_path)
            candidate_predictor = CandidatePredictorRW(candidate_model, sentence_chunker)

        indi_quo = IndiQuo(candidate_predictor, ScenePredictorDummy())

    elif compare_approach == 'scene':
        candidate_predictor = CandidatePredictorDummy(sentence_chunker)
        scene_model = SentenceTransformer(scene_model_path)
        scene_predictor = ScenePredictor(drama, scene_model, 10)
        indi_quo = IndiQuo(candidate_predictor, scene_predictor)
    elif compare_approach == 'full':
        candidate_tokenizer = AutoTokenizer.from_pretrained(candidate_model_path)
        candidate_model = AutoModelForSequenceClassification.from_pretrained(candidate_model_path)
        candidate_predictor = CandidatePredictor(candidate_tokenizer, candidate_model, sentence_chunker,
                                                 add_context, max_candidate_length)

        scene_model = SentenceTransformer(scene_model_path)
        scene_predictor = ScenePredictor(drama, scene_model, 10)

        indi_quo = IndiQuo(candidate_predictor, scene_predictor)
    elif compare_approach == 'sum':
        summaries = []
        with open(summaries_file_path, 'r') as summary_file:
            reader = csv.reader(summary_file, delimiter='\t')
            next(reader)

            for row in reader:
                act, scene = drama.get_scene_act_for_text(row[0])
                if act == -1 or scene == -1:
                    raise IndiQuoException('Could not determine act or scene')
                summaries.append((act, scene, row[1]))

        candidate_model = SentenceTransformer(candidate_model_path)
        candidate_predictor = CandidatePredictorSum(summaries, candidate_model, sentence_chunker)
        indi_quo = IndiQuoSum(candidate_predictor)

    if isfile(target_path) and target_path.endswith('.txt'):
        with open(target_path, 'r', encoding='utf-8') as target_file:
            target_file_content = target_file.read()

        filename = splitext(basename(target_path))[0]
        __process_file(indi_quo, filename, target_file_content, output_folder_path)
    elif isdir(target_path):
        for fileOrFolder in listdir(target_path):
            target_file_path = join(target_path, fileOrFolder)

            if isfile(target_file_path) and target_file_path.endswith('.txt'):
                with open(target_file_path, 'r', encoding='utf-8') as target_file:
                    target_file_content = target_file.read()

                filename = splitext(basename(target_file_path))[0]
                __process_file(indi_quo, filename, target_file_content, output_folder_path)


def main(argv=None):
    indiquo_description = ("IndiQuo is a tool for the detection of indirect quotations (summaries and paraphrases)"
                           " between dramas and scholarly works.")

    train_description = 'This command allows the user to train their a custom model.'

    train_candidate_description = 'Train a custom candidate classification model.'
    train_candidate_st_description = 'Train a custom SentenceTransformer model.'
    train_scene_description = 'Tran a custom scene identification model.'

    compare_description = ('This command allows the user to run inference and execute different functionality which is'
                           ' specified in a subcommand.')

    compare_candidate_description = 'Identify candidates for indirect quotations.'
    compare_scene_description = 'Identify the scene of indirect quotations.'
    compare_full_description = 'Identify candidates and corresponding scenes.'
    compare_sum_description = 'Use summaries to identify indirect quotations.'

    argument_parser = ArgumentParser(prog='indiquo', description=indiquo_description)

    argument_parser.add_argument('--log-level', dest='log_level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR',
                                                                           'CRITICAL'],
                                 help='Set the logging level', default='WARNING')

    subparsers_command = argument_parser.add_subparsers(dest='command')
    subparsers_command.required = True

    parser_train = subparsers_command.add_parser('train', help=train_description, description=train_description)

    subparsers_train_model = parser_train.add_subparsers(dest='train_model')
    subparsers_train_model.required = True

    parser_train_candidate = subparsers_train_model.add_parser('candidate', help=train_candidate_description,
                                                               description=train_candidate_description)

    parser_train_candidate.add_argument('train_folder_path', metavar='train-folder-path',
                                        help='Path to the folder with training and validation data')
    parser_train_candidate.add_argument('output_folder_path', metavar='output-folder-path',
                                        help='Path to the output folder of the trained model')
    parser_train_candidate.add_argument('--model', dest='model', default='deepset/gbert-large',
                                        help='Name of the model on huggingface to use as the base model for fine-tuning'
                                             ' (default: %(default)s)')

    # probably not needed as this did not perform well
    parser_train_st = subparsers_train_model.add_parser('candidate_st', help=train_candidate_st_description,
                                                        description=train_candidate_st_description)

    parser_train_st.add_argument('train_folder_path', metavar='train-folder-path',
                                 help='Path to the folder with training and validation data')
    parser_train_st.add_argument('output_folder_path', metavar='output-folder-path',
                                 help='Path to the output folder of the trained model')
    parser_train_st.add_argument('--model', dest='model', default='deutsche-telekom/gbert-large-paraphrase-cosine',
                                 help='Name of the model on huggingface to use as the base model for fine-tuning'
                                      ' (default: %(default)s)')

    parser_train_scene = subparsers_train_model.add_parser('scene', help=train_scene_description,
                                                           description=train_scene_description)

    parser_train_scene.add_argument('train_folder_path', metavar='train-folder-path',
                                    help='Path to the folder with training and validation data')
    parser_train_scene.add_argument('output_folder_path', metavar='output-folder-path',
                                    help='Path to the input folder')
    parser_train_scene.add_argument('--model', dest='model', default='deutsche-telekom/gbert-large-paraphrase-cosine',
                                    help='Name of the model on huggingface to use as the base model for fine-tuning'
                                         ' (default: %(default)s)')

    parser_compare = subparsers_command.add_parser('compare', help=compare_description,
                                                   description=compare_description)

    subparsers_compare_approach = parser_compare.add_subparsers(dest='compare_approach')
    subparsers_compare_approach.required = True

    cp_all = argparse.ArgumentParser(add_help=False)
    cp_all.add_argument('source_file_path', metavar='source-file-path', help='Path to the source xml drama file')
    cp_all.add_argument('target_path', metavar='target-path', help='Path to the target text file or folder')

    cp_candidate_full = argparse.ArgumentParser(add_help=False)
    cp_candidate_full.add_argument('--add-context', dest='add_context', default=True,
                                action=BooleanOptionalAction, help='If set, candidates are embedded in context up to'
                                                                   ' a total length of --max-candidate-length')
    cp_candidate_full.add_argument('--max-candidate-length', dest='max_candidate_length', default=128,
                                type=int, help='Maximum length in words of a candidate (default: %(default)d)')

    cp_candidate_model = argparse.ArgumentParser(add_help=False)
    cp_candidate_model.add_argument('candidate_model', metavar='candidate-model', default='Fredr0id/indiquo-candidate',
                                help='Name of the model to load from Hugging Face or path to the model folder (default: %(default)s).')
    cp_scene_model = argparse.ArgumentParser(add_help=False)
    cp_scene_model.add_argument('scene_model', metavar='scene-model', default='Fredr0id/indiquo-scene',
                                help='Name of the model to load from Hugging Face or path to the model folder (default: %(default)s).')
    cp_output = argparse.ArgumentParser(add_help=False)
    cp_output.add_argument('output_folder_path', metavar='output-folder-path',
                                help='The output folder path.')

    parser_compare_candidate = (
        subparsers_compare_approach.add_parser('candidate',
                                               parents=[cp_all, cp_candidate_model, cp_output, cp_candidate_full],
                                               help=compare_candidate_description, description=compare_candidate_description)

    )
    parser_compare_candidate.add_argument('--model-type', choices=['st', 'rw', 'iq'], dest='model_type',
                              default='iq', help='The model type to use for candidate prediction.')

    parser_compare_scene = (
        subparsers_compare_approach.add_parser('scene',
                                               parents=[cp_all, cp_scene_model, cp_output],
                                               help=compare_scene_description, description=compare_scene_description)
    )

    parser_compare_full = (
        subparsers_compare_approach.add_parser('full',
                                               parents=[cp_all, cp_candidate_model, cp_scene_model, cp_output, cp_candidate_full],
                                               help=compare_full_description, description=compare_full_description)
    )

    parser_compare_sum = (
        subparsers_compare_approach.add_parser('sum',
                                               parents = [cp_all, cp_candidate_model, cp_output],
                                               help=compare_sum_description, description=compare_sum_description)
    )
    parser_compare_sum.add_argument('--summaries-file-path', dest='summaries_file_path', required=True,
                                help='Path to the summaries tsv file.')

    args = argument_parser.parse_args(argv)

    log_level = args.log_level
    logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if args.command == 'train':
        if args.train_model == 'candidate' or args.train_model == 'candidate_st' or args.train_model == 'scene':
            train_folder_path = args.train_folder_path
            output_folder_path = args.output_folder_path
            model = args.model
            model_name_repl = model.replace('/', '')

            now = datetime.now()
            date_time_string = now.strftime('%Y_%m_%d_%H_%M_%S')
            date_time_string += f'_{model_name_repl}'
            output_folder_path = join(output_folder_path, date_time_string)
            Path(output_folder_path).mkdir(parents=True, exist_ok=True)

            if args.train_model == 'candidate':
                __train_candidate(train_folder_path, output_folder_path, model)
            elif args.train_model == 'candidate_st':
                __train_candidate_st(train_folder_path, output_folder_path, model)
            elif args.train_model == 'scene':
                __train_scene(train_folder_path, output_folder_path, model)

    elif args.command == 'compare':
        source_file_path = args.source_file_path
        target_path = args.target_path
        output_folder_path = args.output_folder_path

        c_appr = args.compare_approach

        candidate_model_folder_path = None
        if c_appr in ['candidate', 'full', 'sum']:
            candidate_model_folder_path = args.candidate_model_folder_path

        scene_model_folder_path = None
        if c_appr in ['scene', 'full']:
            scene_model_folder_path = args.scene_model_folder_path

        add_context = True
        max_candidate_length = 128
        if c_appr in ['candidate', 'full']:
            add_context = args.add_context
            max_candidate_length = args.max_candidate_length

        model_type = None
        if c_appr == 'candidate':
            model_type = args.model_type

        summaries_file_path = None
        if c_appr == 'sum':
            summaries_file_path = args.summaries_file_path

        now = datetime.now()
        date_time_string = now.strftime('%Y_%m_%d_%H_%M_%S')
        output_folder_path = join(output_folder_path, date_time_string)
        Path(output_folder_path).mkdir(parents=True, exist_ok=True)

        __run_compare(c_appr, model_type, source_file_path, target_path, candidate_model_folder_path, scene_model_folder_path,
                      output_folder_path, add_context, max_candidate_length, summaries_file_path)


if __name__ == '__main__':
    sys.exit(main())

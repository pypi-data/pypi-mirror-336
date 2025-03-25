import math
from os.path import join

from sentence_transformers import SentenceTransformer, InputExample, losses, evaluation
from torch.utils.data import DataLoader
import csv


def train(train_folder_path: str, output_folder_path: str, model_name: str):

    train_examples = []
    with open(join(train_folder_path, 'train_set.tsv'), 'r') as train_file:
        reader = csv.reader(train_file, delimiter='\t')

        for row in reader:
            ie = InputExample(texts=[row[0], row[1]], label=int(row[2]))
            train_examples.append(ie)

    val_sentences_1 = []
    val_sentences_2 = []
    val_labels = []
    with open(join(train_folder_path, 'val_set.tsv'), 'r') as train_file:
        reader = csv.reader(train_file, delimiter='\t')

        for row in reader:
            val_sentences_1.append(row[0])
            val_sentences_2.append(row[1])
            val_labels.append(int(row[2]))

    model = SentenceTransformer(model_name)
    train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)
    train_loss = losses.ContrastiveLoss(model=model)

    evaluator = evaluation.BinaryClassificationEvaluator(val_sentences_1, val_sentences_2, val_labels)

    num_epochs = 5
    warmup_steps = math.ceil(len(train_dataloader) * num_epochs * 0.1)  # 10% of train data for warm-up
    model.fit(train_objectives=[(train_dataloader, train_loss)], epochs=num_epochs, warmup_steps=warmup_steps,
              evaluator=evaluator, output_path=output_folder_path)

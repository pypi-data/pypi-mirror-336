# Readme
This repository contains the tool `IndiQuo` for the detection of indirect quotations (summaries and paraphrases)
between dramas from [DraCor](https://dracor.org) and scholarly works which interpret the drama.

## Installation
~~~
pip install indiquo
~~~

### Dependencies
The dependencies to run the [Rederwiedergabe Tagger](https://github.com/redewiedergabe/tagger) are not installed by
default as this can be a [tricky process](https://github.com/redewiedergabe/tagger/issues/4) and this tagger is only
used as a baseline and not for our approach and therefore not needed in most cases.

## Usage
The following sections describe how to use IndiQuo on the command line.

### Training
The library supports training of custom models for candidate identification and scene prediction.

#### Candidate Identification

~~~
indiquo train candidate
path_to_train_folder
path_to_the_output_folder
hugginface_model_name
~~~

`path_to_train_folder` has to contain to files named `train_set.tsv` and `val_set.tsv` which contain one example per
line in the form a string and a label, tab separated, for example:

~~~
Some positive example	1
Some negative example	0
~~~

`hugginface_model_name` is the name of the model on huggingface to use for fine-tuning, `deepset/gbert-large` is used
as the default.

#### Scene Prediction

~~~
indiquo train scene
path_to_train_folder
path_to_the_output_folder
hugginface_model_name
~~~

`path_to_train_folder` has to contain to files named `train_set.tsv` and `val_set.tsv` which contain one example per
line in the form two strings, a drama excerpt and a corresponding summary, tab separated, for example:

~~~
Drama excerpt	Summary
~~~

`hugginface_model_name` is the name of the model on huggingface to use for fine-tuning,
`deutsche-telekom/gbert-large-paraphrase-cosine` is used  as the default.

### Indirect Quotation Identification

To run `IndiQuo` inference with the default models, use the following command:

~~~
indiquo compare full path_to_drama_xml path_to_target_text output_path
~~~

<details>
<summary>All IndiQuo command line options</summary>

~~~
usage: indiquo compare full [-h] [--add-context | --no-add-context]
                            [--max-candidate-length MAX_CANDIDATE_LENGTH]
                            source-file-path target-path candidate-model
                            scene-model output-folder-path

Identify candidates and corresponding scenes.

positional arguments:
  source-file-path      Path to the source xml drama file
  target-path           Path to the target text file or folder
  candidate-model       Name of the model to load from Hugging Face or path to
                        the model folder (default: Fredr0id/indiquo-
                        candidate).
  scene-model           Name of the model to load from Hugging Face or path to
                        the model folder (default: Fredr0id/indiquo-scene).
  output-folder-path    The output folder path.

options:
  -h, --help            show this help message and exit
  --add-context, --no-add-context
                        If set, candidates are embedded in context up to a
                        total length of --max-candidate-length
  --max-candidate-length MAX_CANDIDATE_LENGTH
                        Maximum length in words of a candidate (default: 128)
~~~

</details>

The output folder will contain a tsv file for each txt file in the target path. The tsv files have the following
structure:

The output will look something like this:

~~~
start   end text        score   scenes
10      15  some text   0.5     1:1:0.2#2:5:0.5#...
~~~

The first three columns are the character start and end positions and the text of the quotation in the target text. The
fourth column is the probability of the positive class, i.e., the candidate is an indirect quotation. The last column
contains the top 10 source scenes separated by '#' and each part has the following structure: act:scene:probability. 

### Baselines and reproduction

It is possible to only run the candidate classification step with the command `compare candidate`. With the option
`--model-type` it is possible to run the base models (rw=rederwiedergabe, st=SentenceTransformer).

With the command `compare sum` a SentenceTransformer with summaries can be used.

## Citation
If you use the code in repository or base your work on our code, please cite our paper:
~~~
TBD
~~~
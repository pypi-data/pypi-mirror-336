from transformers import AutoTokenizer, DataCollatorWithPadding, AutoModelForSequenceClassification, TrainingArguments, Trainer
from datasets import load_dataset
import evaluate
import numpy as np


def __preprocess_function(examples, tokenizer):
    return tokenizer(examples["text"], truncation=True)


def __prepare_compute_metrics(eval_metric):
    def custom_compute_metrics(eval_pred):
        predictions, labels = eval_pred
        predictions = np.argmax(predictions, axis=1)
        return eval_metric.compute(predictions=predictions, references=labels)

    return custom_compute_metrics


def train(train_folder_path: str, output_folder_path: str, model_name: str):

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    special_tokens_dict = {'additional_special_tokens': ['<Q>', '</Q>']}
    tokenizer.add_special_tokens(special_tokens_dict)

    dataset = load_dataset(train_folder_path, data_files={'train': 'train_set.tsv', 'validation': 'val_set.tsv'}, delimiter='\t')
    tokenized_dataset = dataset.map(__preprocess_function, batched=True, fn_kwargs={'tokenizer': tokenizer})

    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
    model.resize_token_embeddings(len(tokenizer))

    eval_metric = evaluate.load('f1')
    custom_compute_metrics = __prepare_compute_metrics(eval_metric)

    training_args = TrainingArguments(
        output_dir=output_folder_path,
        learning_rate=2e-5,
        warmup_ratio=0.1,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=5,
        weight_decay=0.01,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        save_total_limit=2,
        load_best_model_at_end=True,
        metric_for_best_model='eval_f1',
        push_to_hub=False,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset['train'],
        eval_dataset=tokenized_dataset['validation'],
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_metrics=custom_compute_metrics
    )

    trainer.train()

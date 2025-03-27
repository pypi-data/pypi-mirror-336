from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from transformers import AutoTokenizer, TrainingArguments, Trainer
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, TaskType
import torch

class OptiNet:
    def __init__(self, model, model_name='model', model_type='ml'):
        self.model = model
        self.model_name = model_name
        self.model_type = model_type
        if self.model_type == 'llm':
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def prepare_data(self, **kwargs):
        if self.model_type == 'ml':
            # User must pass 'X' and 'y' or choose a dataset explicitly
            if 'X' in kwargs and 'y' in kwargs:
                test_size = kwargs.get('test_size', 0.2)
                random_state = kwargs.get('random_state')  # No default, use whatever the user provides
                X_train, X_test, y_train, y_test = train_test_split(
                    kwargs['X'], kwargs['y'], test_size=test_size, random_state=random_state
                )
                return X_train, X_test, y_train, y_test

            elif 'dataset' in kwargs:
                dataset_name = kwargs['dataset']
                if dataset_name == 'digits':
                    data = load_digits()
                    X_train, X_test, y_train, y_test = train_test_split(
                        data.data, data.target, test_size=kwargs.get('test_size', 0.2),
                        random_state=kwargs.get('random_state')
                    )
                    return X_train, X_test, y_train, y_test
                else:
                    raise NotImplementedError(f"Built-in dataset '{dataset_name}' not supported.")
            else:
                raise ValueError("Please pass either 'X' and 'y' or a supported built-in 'dataset' name.")

        elif self.model_type == 'llm':
            # If user passes a HuggingFace-style dataset name
            if 'dataset' in kwargs:
                return load_dataset(kwargs['dataset'])

            # Or a preloaded dataset
            elif 'dataset_obj' in kwargs:
                return kwargs['dataset_obj']

            else:
                raise ValueError("Please provide either a 'dataset' name or a 'dataset_obj' to use.")


    def tokenize_data(self, dataset):
        if self.model_type == 'llm':
            def tokenize_function(examples):
                return self.tokenizer(examples["text"], padding="max_length", truncation=True)

            tokenized_datasets = dataset.map(tokenize_function, batched=True)
            tokenized_datasets = tokenized_datasets.remove_columns(["text"])
            tokenized_datasets.set_format("torch")
            return tokenized_datasets

    def train_model(self, X_train, y_train=None, **kwargs):
        if self.model_type == 'ml':
            scaler = StandardScaler()
            X_train = scaler.fit_transform(X_train)
            self.model.fit(X_train, y_train)
            self.scaler = scaler

        elif self.model_type == 'llm':
            # Apply quantization if user provides config
            quant_config = kwargs.pop("quantization_config", None)
            if quant_config:
                from transformers import BitsAndBytesConfig
                bnb_config = BitsAndBytesConfig(**quant_config)
                self.model = self.model.from_pretrained(self.model_name, quantization_config=bnb_config, device_map="auto")

            # Extract and apply LoRA if LoRA-related keys exist
            lora_keys = ["lora_r", "lora_alpha", "lora_dropout", "bias", "task_type", "target_modules"]
            lora_kwargs = {k: kwargs.pop(k) for k in list(kwargs.keys()) if k in lora_keys}
            if lora_kwargs:
                # Add missing required keys or let user handle it (we assume nothing)
                if "task_type" not in lora_kwargs:
                    lora_kwargs["task_type"] = TaskType.SEQ_CLS
                lora_config = LoraConfig(**lora_kwargs)
                self.model = get_peft_model(self.model, lora_config)

            # Prepare Training Arguments
            training_args = TrainingArguments(**kwargs)

            # Train the model
            trainer = Trainer(
                model=self.model,
                args=training_args,
                train_dataset=X_train,
                eval_dataset=y_train,
            )

            trainer.train()
            self.trainer = trainer

    def evaluate_model(self, X_test, y_test=None, **kwargs):
        if self.model_type == 'ml':
            if not hasattr(self, 'model'):
                raise RuntimeError("You need to train the model before evaluating it.")
            X_test = self.scaler.transform(X_test)
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            return accuracy

        elif self.model_type == 'llm':
            results = self.trainer.evaluate(**kwargs)
            return results

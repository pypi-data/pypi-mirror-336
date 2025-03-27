# OptiNet - A Versatile Library for ML and NLP Model Training

OptiNet is a Python library designed to simplify and optimize traditional Machine Learning (ML) and Natural Language Processing (NLP) workflows. With an easy-to-use interface, OptiNet allows you to prepare datasets, train models, and evaluate performance for both ML and large language models (LLMs). This library supports scikit-learn models as well as transformer-based models from Hugging Face, with support for LoRA and QLoRA for parameter-efficient fine-tuning.

## Features

- **Unified Interface**: Train and evaluate both traditional ML models and transformer-based NLP models.
- **Data Preparation**: Quickly load, split, and prepare data for training.
- **Tokenizer Integration**: Easily tokenize text datasets using Hugging Face's transformers for NLP tasks.
- **Model Training**: Train both ML models (e.g., scikit-learn) and large language models using Trainer from Hugging Face.
- **LoRA & QLoRA Support**: Fine-tune large language models with Low-Rank Adaptation (LoRA) and Quantized LoRA (QLoRA) for efficient training.
- **Scalable Evaluations**: Evaluate trained models and get performance metrics like accuracy.

## Installation

You can install OptiNet using pip:

```sh
pip install OptiNet
```

## Usage

### 1. Import and Initialize OptiNet

OptiNet can be used for both ML models (e.g., scikit-learn classifiers) and NLP models (e.g., transformers). Here is how you can get started:

```python
from optinet import OptiNet
from sklearn.ensemble import RandomForestClassifier
from transformers import AutoModelForSequenceClassification

# Example ML Model
ml_model = RandomForestClassifier()
optinet_ml = OptiNet(model=ml_model, model_type='ml')

# Example NLP Model
llm_model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased")
optinet_nlp = OptiNet(model=llm_model, model_type='llm', model_name='distilbert-base-uncased')
```

### 2. Prepare Data

For ML models, OptiNet can load and split datasets like `digits` from scikit-learn:

```python
# Prepare data for ML model
X_train, X_test, y_train, y_test = optinet_ml.prepare_data(dataset='digits')
```

For NLP models, you can load datasets from Hugging Face's `datasets` library:

```python
# Prepare data for NLP model
nlp_dataset = optinet_nlp.prepare_data(dataset='imdb')  # e.g., IMDB movie reviews dataset
```

#### Custom Dataset Support

If you have a custom dataset (e.g., loaded from a file or a database), you can pass the dataset directly using the dataset_obj parameter:

```python
# Prepare data from a custom dataset
my_dataset = load_dataset("csv", data_files="my_custom_data.csv")
nlp_dataset = optinet_nlp.prepare_data(dataset_obj=my_dataset)
```

This approach allows flexibility to use any custom dataset, without being restricted to the built-in ones.

### 3. Tokenize Data (For NLP Models)

If you're working with NLP models, you need to tokenize the data before training:

```python
# Tokenize NLP dataset
tokenized_dataset = optinet_nlp.tokenize_data(nlp_dataset)
```

### 4. Train the Model

You can train both ML and NLP models using the `train_model()` method. This is where you can choose to fine-tune your model with LoRA and QLoRA by passing the relevant parameters.

Train ML model:

```python
# Train ML model
optinet_ml.train_model(X_train, y_train)
```

Train NLP model with LoRA:

```python
# Train NLP model with LoRA fine-tuning
optinet_nlp.train_model(
    tokenized_dataset['train'],
    output_dir="./output_lora",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    lora_r=4,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1,
    task_type="SEQ_CLS"
)
```

Train NLP model with QLoRA (4-bit quantization):

```python
# Train NLP model with QLoRA (using 4-bit quantization)
optinet_nlp.train_model(
    tokenized_dataset['train'],
    output_dir="./output_qlora",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    quantization_config={"load_in_4bit": True, "bnb_4bit_compute_dtype": torch.float16},
    lora_r=4,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1,
    task_type="SEQ_CLS"
)
```

### 5. Evaluate the Model

Evaluate the performance of your trained model:

```python
# Evaluate ML model
accuracy = optinet_ml.evaluate_model(X_test, y_test)
print(f"ML Model Accuracy: {accuracy:.2f}")

# Evaluate NLP model
results = optinet_nlp.evaluate_model(tokenized_dataset['test'])
print("NLP Model Evaluation:", results)
```

## Requirements

OptiNet depends on several popular Python packages for ML and NLP tasks:

- `scikit-learn`
- `transformers`
- `datasets`
- `torch`
- `peft` (for LoRA and QLoRA support)

To install these requirements, you can use the following command:

```sh
pip install scikit-learn transformers datasets torch peft
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- Vishwanath Akuthota
- Ganesh Thota
- Krishna Avula

## Contributing

We welcome contributions to improve OptiNet. Please feel free to submit issues and pull requests on the GitHub repository.
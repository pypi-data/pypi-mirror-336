# SAIS Prism SDK

[![PyPI version](https://img.shields.io/pypi/v/sais-prism-sdk)](https://pypi.org/project/sais-prism-sdk/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Unified Interface for ML Lifecycle Management

### Background
In today’s data-driven AI era, model development has evolved from traditional single-model training into a complex end-to-end engineering process. As AI applications deepen in industrial scenarios, data governance in the traditional internet domain has primarily focused on storage layers such as data warehouses and data lakes. However, data governance in industrialized AI scenarios is far more intricate. Beyond managing the storage and governance of raw data, it also involves handling intermediate data generated during feature engineering, versioning of training datasets, and more. The quality of this data directly impacts model performance.

Compared to data applications in the traditional internet domain, the data pipeline in AI for Science (AI4S) scenarios is longer and more interdependent. From the collection of raw data to the training data processed through feature engineering, to the experimental data generated during model training, and finally to the deployed model files—each step produces a vast array of assets that require tracking and management. This complexity necessitates the establishment of a comprehensive data and model management system.

### Problem Statements
- [Fragmented Training](#fragmented-training) : The current machine learning (ML) training process is disjointed and lacks a unified management approach. Algorithm developers are operating in a "black box" manner, with no standardized specifications for training code, environment setup, or scenario definitions. Everyone is working independently, leading to inconsistent training standards, uncoordinated code management, and a lack of model standardization.
- [Incomplete Data and Model Lifecycle](#incomplete-data-and-model-lifecycle) : Data used in each ML process (metadata), such as file paths, versions, and specific files, is not centrally recorded and is instead scattered across individual personal directories. Similarly, training-related parameters, metrics, and statuses (including model training status and data lifecycle states like quality) associated with models are inadequately tracked, making it difficult to ensure consistency and reliability.
- [Lack of Visualized Management](#lack-of-visualized-management) : Currently, operations are command-line based, with no clear visual interface for managing models and data. Elements such as checkpoints, performance indicators, and versions from the training process cannot be effectively retrieved, shared, or served, exacerbating the management challenges.


### Features

- 🚀 Centralized Configuration Management [Done]
- 🔄 Auto MLflow Integration [Done]
- 📦 Extensible Data Access Layer [Progress]
- 🧩 Declarative Experiment Tracking [Done]
- 📚 Hierarchical Dependency Management [Done]

### Architecture Design

![Architecture Diagram](img/arc.png)


### Doc
[sais-prism-sdk](https://c0fu1j3a9m0.feishu.cn/wiki/KnC3wWegVijdPtkPH2XcktE7nGe?from=from_copylink)

### Use Manual

##### Installation

```bash
pip install sais-prism-sdk
```

##### Configuration (example)
The configuration file `sais_foundation.yaml` is mandatory. This file is used to configure the tool for project-level settings. If not found, the tool will throw an error.

There are three main sections in the configuration file: `foundation`, `unified_data_access`, and `ml`. The foundation is used to configure the experiment name, while the unified_data_access section is used to configure the data access settings, and the ml section is used to configure the MLflow settings.
```yaml
foundation:
  experiment_name: lifescience

unified_data_access:
  enabled: false
  token: demo_token
  data_access:
    dataset_names:
    - alpaca_sft_dataset.jsonl
    - mars
ml:
  enabled: true
  auto_log: true
  system_tracing: true
  security:
    enabled: true
    username: lifescience
    password: lifescience_~#
  parameters:
    output_dir: artifacts/runtime
    device: mps
    dataset_names:
    - /cpfs01/projects-HDD/cfff-4a8d9af84f66_HDD/public/Data/ecmwf-001/ENS
    base_model: meta-llama/Llama-3.2-1B-Instruct
    num_train_epochs: 3
    per_device_train_batch_size: 2
    gradient_accumulation_steps: 8
    learning_rate: 2.0e-05
    weight_decay: 0.02
    warmup_steps: 100
    save_total_limit: 1
    logging_dir: ./logs
    logging_steps: 10
    save_strategy: epoch
    evaluation_strategy: no
    report_to:
    - mlflow
    optim: adamw_torch
    gradient_checkpointing: true
  custom_metrics: []
  artifacts: []
  model_repo:
    model_uri: runs:/{run_id}/artifacts/model
    name: llama_models
    await_registration_for: 300
    tag:
      framework: pytorch
      task_type: language-model
      model_type: llama_lifescience
      base_model: meta-llama/Llama-3.2-1B-Instruct
    version: 1.0.1
```

##### Command-line Configuration Override

The SDK supports overriding or adding configuration values directly from the command line without modifying the YAML file. This is useful for quick experimentation or when running in environments where the YAML file cannot be modified.

The configuration override follows the dot notation pattern to access nested configuration items. You can use the following formats:

```bash
# Format 1: Multiple parameters with separate --config flags
python your_script.py --config key.path=value --config another.key=value2

# Format 2: Multiple parameters with a single --config flag
python your_script.py --config key.path=value another.key=value2
```

**Examples:**

1. Override training parameters:
```bash
python examples/sft_training_example.py --config ml.parameters.warmup_steps=100 ml.parameters.weight_decay=0.02
```

2. Change experiment name:
```bash
python examples/sft_training_example.py --config foundation.experiment_name=new_experiment
```

3. Update model repository configuration:
```bash
python examples/sft_training_example.py --config ml.model_repo.name=new_model ml.model_repo.version=1.1.0
```

4. Pass a list as a value (use JSON format):
```bash
python examples/sft_training_example.py --config ml.parameters.dataset_names='["/path/dataset1", "/path/dataset2"]'
```

5. Pass a dictionary as a value:
```bash
python examples/sft_training_example.py --config ml.model_repo.tag='{"framework": "pytorch", "task_type": "classification"}'
```

By default, changes made through command-line overrides are also written back to the YAML file. If you want to apply changes only in memory without modifying the YAML file, you can modify the `parse_cli_args` function call in your script:

```python
from sais_prism.core.config import parse_cli_args

if __name__ == "__main__":
    # Only apply changes in memory, don't update YAML file
    parse_cli_args(update_yaml=False)
    
    # Run your code
    YourClass().run()
```

This feature provides flexibility for experimentation and CI/CD pipelines, allowing you to easily override configuration values without modifying the YAML file directly.

### User Manual

#### Installation
```sh
pip install -r requirements.txt
```

#### Generic code snippet
Using below code snippet as a starting point.
```python
@sais_foundation # Core annotation
def ClassName():
    def run(self):
      # experiment code
if __name__ == "__main__":
    ClassName().run()
```
There is one of examples that uses SFT to train a Llama model on MPS
```python 
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
)
from datasets import load_dataset
from sais_prism.core.service_locator import ServiceLocator # import for single instance
from sais_prism.core.decorators import sais_foundation # import the decorator
from sais_prism.core.config import config  # import the config 

@sais_foundation
class SFTTraining:
    def __init__(self) -> None:
        self.ml = ServiceLocator.get_ml_manager()
        self.ml_config = config.ml

    def run(self):
        # 1. Load model and tokenizer
        tokenizer = AutoTokenizer.from_pretrained(self.ml_config.parameters.base_model)
        tokenizer.pad_token = tokenizer.eos_token  # Set padding token to EOS token

        # Load model with memory optimizations and FP16 precision
        model = AutoModelForCausalLM.from_pretrained(
            self.ml_config.parameters.base_model,
            device_map=self.ml_config.parameters.device,
            low_cpu_mem_usage=True,  # Reduce CPU memory usage
            torch_dtype=torch.float16,  # Use FP16 to lower memory footprint
        )
    
        # 3. Load and preprocess the dataset
        dataset = load_dataset(
            "json", data_files=config.unified_data_access.data_access.dataset_names[0], split="train")


        # Enable gradient checkpointing to save memory
        model.gradient_checkpointing_enable()

        def preprocess_function(examples):
        # Combine instruction and input, handling cases where input is empty
            inputs = [
                f"{instruction}\n{input}" if input else instruction
                for instruction, input in zip(examples["instruction"], examples["input"])
            ]
            # Tokenize inputs and outputs
            model_inputs = tokenizer(
                inputs,
                text_target=examples["output"],  # Target is the output field
                truncation=True,
                padding="max_length",  # Fixed-length padding to avoid dynamic memory allocation
                max_length=256,  # Smaller max length to reduce memory usage
                return_tensors="pt",  # Return PyTorch tensors directly
            )
            return model_inputs


        # Preprocess dataset with caching and multithreading
        tokenized_datasets = dataset.map(
            preprocess_function,
            batched=True,
            num_proc=4,  # Use multiple threads (adjust based on CPU cores)
            remove_columns=dataset.column_names,  # Remove original columns to save memory
        )

        # 4. Set up data collator
        data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

        # 5. Define training arguments
        training_args = TrainingArguments(
            output_dir=self.ml_config.parameters.output_dir,
            num_train_epochs=self.ml_config.parameters.num_train_epochs,  # Number of training epochs
            per_device_train_batch_size=self.ml_config.parameters.per_device_train_batch_size,  # Small batch size to fit in memory
            gradient_accumulation_steps=self.ml_config.parameters.gradient_accumulation_steps,  # Accumulate gradients to simulate larger batch size
            learning_rate=self.ml_config.parameters.learning_rate,
            weight_decay=self.ml_config.parameters.weight_decay,
            warmup_steps=self.ml_config.parameters.warmup_steps,  # Reduced warmup steps
            save_total_limit=self.ml_config.parameters.save_total_limit,  # Keep only one checkpoint
            logging_dir=self.ml_config.parameters.logging_dir,
            logging_steps=self.ml_config.parameters.logging_steps,  # Log less frequently to save resources
            save_strategy=self.ml_config.parameters.save_strategy,  # Save at the end of each epoch
            evaluation_strategy=self.ml_config.parameters.evaluation_strategy,  # No evaluation during training
            report_to=self.ml_config.parameters.report_to,  # Disable reporting to external tools
            optim=self.ml_config.parameters.optim,  # Optimized AdamW optimizer
            # Enable gradient checkpointing (consistent with model)
            gradient_checkpointing=self.ml_config.parameters.gradient_checkpointing,
        )

        # 6. Initialize and run the trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_datasets,
            data_collator=data_collator,
            callbacks=[self.ml],  # Use MLflowManager as callback
        )

        # Clear memory and start training
        if torch.cuda.is_available():
            torch.cuda.empty_cache()  # Clear GPU memory if available
        trainer.train()

        # 7. Save the fine-tuned model and tokenizer
        model.save_pretrained("./fine_tuned_model")
        tokenizer.save_pretrained("./fine_tuned_model")

        print("Done")
        
if __name__ == "__main__":
    sft = SFTTraining()
    sft.run()
```


### API Reference

| Class | Description |
|-------|-------------|
| `ConfigManager` | Central config access |
| `MLflowService` | Model registry & tracking |
| `DataClient` | Unified data interface |

### Core Components

- `ConfigManager`: Centralized configuration management
- `MLflowService`: Model registry and tracking
- `DataClient`: Unified data access interface


### Service Locator

```python
class ServiceLocator:
    _ml_instance: Optional[MLflowManager] = None
    _data_client_instance: Optional[DataAccessClient] = None

    @classmethod
    def get_ml_manager(cls) -> MLflowManager:
        if not cls._ml_instance:
            cls._ml_instance = MLflowManager(config.ml)
        return cls._ml_instance
```

### MLflow Configuration

```yaml
ml:
  enabled: true
  auto_log: true
  system_tracing: true
  parameters:
    key: value
    ...
  custom_metrics: [] # Define custom metrics
  artifacts: [] 
  model_repo:
    model_uri: "runs:/{run_id}/artifacts/model"
    name: "model_name"
    await_registration_for: 300
    tag:
      key: value
      ...
    version: 
```

### Data Access Configuration
Notice: this is still under development
```yaml
data_access:
  enabled: true
  cached: true  # Enable local caching
  token: ${ENV_API_TOKEN}  # Env var injection
  data_access: [dataset_name, dataset_name, ...]
```

Register with service locator:
```python
ServiceLocator.set_data_client(CustomDataClient())
```

## Model Evaluation

After training your SFT model, you can evaluate its performance using our evaluation framework. The SDK provides tools to generate custom evaluation datasets and measure model performance against standardized metrics.

### Step 1: Generate Evaluation Dataset

First, create an evaluation dataset using the `generate_evaluation_dataset.py` script:

```bash
python examples/generate_evaluation_dataset.py --output examples/evaluation_dataset.jsonl
```

This script generates a JSONL file containing pharmaceutical domain test questions for evaluating your model. You can:
- Control the number of questions with `--num_questions`
- Customize the output path with `--output`
- Modify the script to add your own domain-specific questions

The evaluation dataset follows this format:
```json
{"instruction": "What are the different classifications of the drug Imatinib?", "input": "", "output": "Expected detailed response about Imatinib classifications..."}
```

### Step 2: Run Model Evaluation

Evaluate your fine-tuned model against the evaluation dataset:

```bash
python examples/evaluate_sft_model.py --model_path ./fine_tuned_model --evaluation_file examples/evaluation_dataset.jsonl
```

Additional command-line options:
- `--max_samples N`: Limit the number of samples to evaluate
- `--max_new_tokens N`: Set maximum generation length (default: 200)
- `--output_file PATH`: Specify custom output file path

### Step 3: Review Evaluation Results

The evaluation script calculates performance metrics including:

1. **ROUGE scores** (measuring text overlap with reference answers):
   - ROUGE-1: Word unigram overlap
   - ROUGE-2: Word bigram overlap
   - ROUGE-L: Longest common subsequence

2. **BLEU score** (measuring translation quality)

3. **Generation performance**:
   - Tokens per second
   - Generation time

Sample evaluation summary from a recent run:
```
===== EVALUATION SUMMARY =====
rouge1: 0.2845
rouge2: 0.1421
rougeL: 0.2234
bleu: 0.0857
avg_tokens_per_second: 21.98
avg_generation_time: 9.10
total_samples: 10

Detailed results saved to artifacts/sft_evaluation_results_20250226_105423.json
```

### Evaluation Artifacts and Storage

Following project standards, all evaluation artifacts are stored in the `artifacts` directory with appropriate metadata:

1. **Evaluation Results**: The JSON file containing detailed evaluation metrics is stored with proper versioning according to semver standards
   ```
   artifacts/evaluation_results/sft_evaluation_results_v1.0.1_20250226.json
   ```

2. **Model Metadata**: Each evaluation includes tags for:
   - Framework (pytorch)
   - Task type (language-model)
   - Base model
   - Evaluation dataset information

3. **MLflow Integration**: All evaluation metrics are automatically tracked in MLflow, allowing for:
   - Comparison between model versions
   - Visualization of performance trends
   - Correlation between hyperparameters and evaluation metrics


### Example Evaluation Question and Response

```
===== QUESTION 1 =====
Instruction: What are the different classification types associated with the investigational drug AR-12?

Model response:
The investigational drug AR-12 is classified into different types based on its pharmacological profile, mechanism of action, and potential therapeutic applications. Here are some of the different classification types associated with AR-12:

1. **Antiviral**: AR-12 is classified as an antiviral drug...
[truncated]

Reference answer:
AR-12 is classified as a small molecule inhibitor targeting PDK1 in the PI3K/AKT pathway. It's also categorized as an anti-cancer agent, anti-viral compound, and autophagy modulator.

Metrics:
rouge1: 0.2845
rouge2: 0.1421
rougeL: 0.2234
bleu: 0.0857
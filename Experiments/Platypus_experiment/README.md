# Platypus: Quick, Cheap, and Powerful Refinement of LLMs

The Platypus models are a series of fine-tuned and merged variants based on the LLaMA and LLaMa-2 transformer architectures. Platypus takes advantage of [LoRA](https://arxiv.org/pdf/2106.09685.pdf) and [PEFT](https://github.com/huggingface/peft). 

All base models are available via HuggingFace: [`garage-bAInd`](https://huggingface.co/garage-bAInd)

This Technique was used to fine tune [Llama-2-13b](https://huggingface.co/meta-llama/Llama-2-13b-hf) with 1k data entries, for our problem statement. For dataset and generation techniques, refer the data folder.
## Methodology
Our methodology employs Low Rank Approximation (LoRA) for training efficiency, involving freezing pre-trained model weights and incorporating rank decomposition matrices.
State-of-the-art Parameter-Efficient Fine-Tuning (PEFT) is utilized for model merging, taking advantage of the PEFT library's built-in capabilities.
Fine-tuning initially focused on attention modules and expanded to other modules based on performance analysis.
Hyperparameters were carefully chosen, and Alpaca's prompt formatting template ensured consistency.
The fine-tuning process utilized the Hugging Face transformers library for compatibility and efficiency.

## Local Setup

This repository is multi-GPU friendly, and provides code to use model or data parellelism, depending on your computational resources. 

1. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

2. Be sure to use these exact requirements or you may run into model saving or OOM issues.

## Fine-tuning (`finetune.py`)

Run `fine-tuning.sh`.

Note: The script above uses `torchrun` for data parallelism. PyTorch is not in `requirements.txt` since technically you can run fine-tuning without it (after a few minor changes to the .py file). To use `fine-tuning.sh`, [PyTorch](https://pytorch.org/get-started/locally/) needs to be installed. `torchrun` is recommended for parallelisation of training, but `accelerate` can also be used. 

Hyperparameters used to fine-tune Platypus:

| Hyperparameter      | Values |
|---------------------|--------|
| learning rate       | 4e-4   |
| batch size          | 16     |
| microbatch  size    | 1      |
| warmup steps        | 100    |
| epochs              | 1,5      |
| weight decay        | 0.     |
| lr scheduler        | cosine |
| lora alpha          | 16     |
| lora rank           | 16     |
| lora dropout        | 0.05   |
| lora target modules | gate_proj, up_proj, down_proj|
| cutoff length       | 4096   |
| train on inputs     | False  |
| group by length     | False  |
| add eos token       | False  |

Hardware Specifications for training - 

| Specification      | Values |
|---------------------|--------|
| GPU               | A6000 (48 GB VRAM)  |
| Number of GPUs    | 4 |
| RAM               | 180 GB | 
| Time taken for training | 1 hour |
| Model size after training | 49 GB |

## Merging

Once fine-tuning is complete, `merge.sh` is used to merge the LoRA weights back into the base LLaMa model for export to HuggingFace format.

**NOTE:** (peft should always be installed from source).

# CLI 

[Fastchat](https://github.com/lm-sys/FastChat) provides a simple setup for those interested in running the model. After downloading the model through HuggingFace, clone the Fastchat repository:

```
git clone https://github.com/lm-sys/FastChat.git
cd FastChat
```

Download the required packages:

```
pip3 install --upgrade pip  # enable PEP 660 support
pip3 install -e .
```

Finally, run the following:

```
python3 -m fastchat.serve.cli --model-path garage-bAInd/Platypus-30B --conv-template alpaca

```

## Sample Results

##### Instruction: Search for objects related to the customer CustomerABC and create action items from the search results.

##### Response: 
[
  {
    "tool_name": "search",
    "arguments": [
      {
        "argument_name": "customer",
        "argument_value": "CustomerABC"
      }
    ]
  },
  {
    "tool_name": "action_item",
    "arguments": [
      {
        "argument_name": "objects",
        "argument_value": "$$PREV[0]"
      }
    ]
  }
]
##### Instruction: Find all work items in the testing stage that are related to parts PART-1 and PART-2 and summarize them.

##### Response: 
[
  {
    "tool_name": "search",
    "arguments": [
      {
        "argument_name": "stage",
        "argument_value": "testing"
      },
      {
        "argument_name": "related_to",
        "argument_value": "\$$PREV[0]"
      }
    ]
  }
  {
    "tool_name": "summarize",
    "arguments": [
      {
        "argument_name": "objects",
        "argument_value": "$$PREV[1]"
      }
    ]
  }
]

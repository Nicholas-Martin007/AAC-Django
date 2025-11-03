from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModelForCausalLM, PeftModelForSeq2SeqLM

from fine_tuned.f_model import FinetuneModel
from fine_tuned.f_tokenizer import FinetuneTokenizer

import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

MODEL_PATH = {
    "llama3.2-1b": "meta-llama/Llama-3.2-1B-Instruct",  # 1.24B parameters
    "llama3.2-3b": "meta-llama/Llama-3.2-3B-Instruct",  # 3.21B parameters
    "mistral7b": "mistralai/Mistral-7B-Instruct-v0.3",  # 7.25B parameters
    "flan-large": "google/flan-t5-large",  # 783M parameters
    "flan-xl": "google/flan-t5-xl",  # 2.85B parameters
}


def get_model_path(model_name, experiment):
    if model_name == "llama":
        model_path = MODEL_PATH["llama3.2-3b"]
        if experiment == 1:
            qlora_model_path = r"C:\Users\Nicmar\Documents\coding\QLoRA_Model\V1_QLoRA\llama_downloads\llama3_2-3b_lr0_00025461989761985766_wd0_01_r48_a24_ep2_bs4"
        else:
            qlora_model_path = r"C:\Users\Nicmar\Documents\coding\QLoRA_Model\V2_QLoRA\llama_downloads\llama3_2-3b_lr0_00034608371233975127_wd0_0_r32_a16_ep2_bs2"

    elif model_name == "mistral":
        model_path = MODEL_PATH["mistral7b"]
        if experiment == 1:
            qlora_model_path = r"C:\Users\Nicmar\Documents\coding\QLoRA_Model\V1_QLoRA\mistral_downloads\mistral7b_lr0_00015079044135156433_wd0_1_r64_a128_ep1_bs2"
        else:
            qlora_model_path = r"C:\Users\Nicmar\Documents\coding\QLoRA_Model\V2_QLoRA\mistral_downloads\mistral7b_lr0_00031777491797078413_wd0_04_r16_a8_ep2_bs4"

    else:
        model_path = MODEL_PATH["flan-large"]
        if experiment == 1:
            qlora_model_path = r"C:\Users\Nicmar\Documents\coding\QLoRA_Model\V1_QLoRA\flan-t5_downloads\flan-large_lr0_0001482178201997769_wd0_09_r32_a16_ep1_bs4"
        else:
            qlora_model_path = r"C:\Users\Nicmar\Documents\coding\QLoRA_Model\V2_QLoRA\flan-t5_downloads\flan-large_lr7_789020928835203e-05_wd0_07_r16_a32_ep2_bs4"

    return model_path, qlora_model_path


def load_model(model_name="llama", experiment=2, quantized_version=False):
    model_path, qlora_model_path = get_model_path(model_name, experiment)

    tokenizer = FinetuneTokenizer(
        model_path,
    ).get_tokenizer()

    if "flan" in model_path or "t5" in model_path:
        model_type = "seq2seq"
    else:
        model_type = "causal"

    f_model = FinetuneModel(
        tokenizer=tokenizer,
        model_path=model_path,
        device=DEVICE,
        model_type=model_type,
        quantized_version=quantized_version,
    )

    qlora_model = PeftModelForCausalLM.from_pretrained(
        f_model.model,
        qlora_model_path,
        device_map=DEVICE,
        inference_mode=False,
    )

    merged_model = qlora_model.merge_and_unload()
    merged_model = merged_model.to(DEVICE)

    return tokenizer, merged_model

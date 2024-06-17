from transformers import GPT2LMHeadModel, GPT2Tokenizer, TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments
import pandas as pd

data =pd.read_csv("./data-set/services_rows.csv")


data =  data[[
    "name",
    "price",
    "description",
]]

data["tag"] = data["name"] + " " + data["description"] 

data.drop(columns=["name", "description"], inplace=True)

print(data)

# Load pre-trained model and tokenizer
model = GPT2LMHeadModel.from_pretrained("NlpHUST/gpt2-vietnamese")
tokenizer = GPT2Tokenizer.from_pretrained("NlpHUST/gpt2-vietnamese")

# Prepare training data
dataset = TextDataset(
    tokenizer=tokenizer,
    file_path=None,
    block_size=128,
    data=data["tag"].tolist()
)

##  - Qwen/Qwen-VL-Cha
##  - vinai/PhoGPT-4B-Chat c
##  - openai-community/gpt2
##  - NlpHUST/gpt2-vietnamese

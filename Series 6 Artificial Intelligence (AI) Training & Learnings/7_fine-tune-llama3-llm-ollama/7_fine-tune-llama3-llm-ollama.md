# Project 7: Fine-tuning (Building) LLM Model with Ollama
# --------------------------------------------
# --------------------------------------------
# Folder: 
7_fine-tune-llama3-llm-ollama

# Tools used:
Use google colab for finetuning!
Use unsloth for helping fine-tuning a model!
Use wandb.ai for data visuals: https://wandb.ai/authorize?ref=models

# Youtube reference (Theory)
https://www.youtube.com/watch?v=u5Vcrwpzoz8  <- Llam3 with private knowledge

# Two ways to give LLM Knowledge:
1. Pre-Training (Wikipedia, books, articles, internet) - Gives precise data
2. In Context Learning - Fix the model, put knowledge into the prompt (RAG?) using vector db

# 1 Data Parsing
1. Use LlamaParse for parsing pdf data (its the best)
2. Use FireCrawl for websites parsing

LlamaParse: https://github.com/run-llama/llama_parse
Firecrawl: https://www.firecrawl.dev/

# 2 Chunk Size
Breaking up a large documents into better performance using chunks for LLM
They cannot be too small or too big! Experiment with the data to find best optimal size!

# 3 Rerank
Send reranker to pass in the best chunks

# 4 Hybrid Search
Vector search + Keyword search

# 5 Agentic RAG
Use Query translation/planning
Use Correctic RAG Agent

Tavily can be used for Web Search by Agentic RAG agents!

# Langgraph Example (17:38mins in video):
Download: ollama pull llam3
Run the model: ollama run llam3
Testing: >>> who made facebook?

# ################ Fine Tuning LLM on Ollama ################

# # Youtube reference (pratical)
https://www.youtube.com/watch?v=pTaSDVz0gok        <- Fine-tuning Ollama (training on your data)

# Original Sample Code
https://drive.google.com/drive/folders/1p4ZilsJsdxB5lH6ZBMdIEJBt0WVUMsDq

They will become worse at general tasks but better at your tasks!

Then you can use your own machine for the training OR use Google Colaboratory:
(which is what I did here!)
https://colab.research.google.com/

unsloth to train the models - https://unsloth.ai/?ref=producthunt

# link to colab ...
https://colab.research.google.com/drive/1s2PsYW3BfgtK-M2hIJiMH0tH5oHKGxQJ

Upload the json file to google drive using the side upload button!
Once uploaded, the file should be in the same folder
Make sure T4 is connected ... 

# For GPU check step output
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None'}")

CUDA available: True
GPU: Tesla T4

# For the Lora Adapters code ...
This code snippet applies LoRA (Low-Rank Adaptation) adapters to the pre-trained language model using Unsloth's FastLanguageModel.get_peft_model function. LoRA is a parameter-efficient fine-tuning technique that significantly reduces the number of trainable parameters by adding small, low-rank matrices to the existing weights.

Here's a breakdown of the arguments:

model: The base pre-trained model to which LoRA adapters will be added.
r=64: Sets the LoRA rank. A higher rank allows for more expressive adapters but requires more memory.
target_modules: Specifies the modules within the model where LoRA adapters will be applied. In this case, it's applied to the attention and feed-forward layers.
lora_alpha=128: The scaling factor for the LoRA updates. It's typically set to twice the LoRA rank.
lora_dropout=0: Sets the dropout rate for the LoRA layers. Unsloth optimizes for a dropout of 0.
bias="none": Specifies how bias is handled in the LoRA layers. "none" is optimized for Unsloth.
use_gradient_checkpointing="unsloth": Enables Unsloth's optimized gradient checkpointing for memory efficiency during training.
random_state=3407: Sets a random seed for reproducibility.
use_rslora=False: Disables Rank-Stabilized LoRA.
loftq_config=None: Disables LoftQ, another quantization technique.
By applying these LoRA adapters, the model can be fine-tuned on a specific task or dataset much more efficiently than fine-tuning the entire model.

# For training using wandb.ai
WandB (weights and biases) is a really cool tool for live visuals of data. Essentially you can log data as something like a training loop runs, and each iteration of the loop (i.e. each time the log function is called) it will update a plot in real time.

# Note!!
For wandb.ai, used normal email and password!

# More information here!
https://docs.wandb.ai/platform/hosting/hosting-options/self-managed

# Training output
==((====))==  Unsloth - 2x faster free finetuning | Num GPUs used = 1
   \\   /|    Num examples = 500 | Num Epochs = 3 | Total steps = 189
O^O/ \_/ \    Batch size per device = 2 | Gradient accumulation steps = 4
\        /    Data Parallel GPUs = 1 | Total batch size (2 x 4 x 1) = 8
 "-____-"     Trainable parameters = 119,537,664 of 3,940,617,216 (3.03% trained)
wandb: WARNING The `run_name` is currently set to the same value as `TrainingArguments.output_dir`. If this was not intended, please specify a different run name by setting the `TrainingArguments.run_name` parameter.
wandb: Logging into wandb.ai. (Learn how to deploy a W&B server locally: https://wandb.me/wandb-server)
wandb: You can find your API key in your browser here: https://wandb.ai/authorize?ref=models
wandb: Paste an API key from your profile and hit enter: ··········
wandb: WARNING If you're specifying your api key in code, ensure this code is not shared publicly.
wandb: WARNING Consider setting the WANDB_API_KEY environment variable, or running `wandb login` from the command line.
wandb: No netrc file found, creating one.
wandb: Appending key for api.wandb.ai to your netrc file: /root/.netrc
wandb: Currently logged in as: grahamjohnson77 (grahamjohnson77-gpjohnsonconsulting) to https://api.wandb.ai. Use `wandb login --relogin` to force relogin
Tracking run with wandb version 0.21.0
Run data is saved locally in /content/wandb/run-20250802_191714-qk73li2c
Syncing run outputs to Weights & Biases (docs)
View project at https://wandb.ai/grahamjohnson77-gpjohnsonconsulting/huggingface
View run at https://wandb.ai/grahamjohnson77-gpjohnsonconsulting/huggingface/runs/qk73li2c
 [189/189 09:20, Epoch 3/3]
Step	Training Loss
25	    0.451400
50	    0.150000
75	    0.135000
100	    0.122500
125	    0.115300
150	    0.111700
175	    0.110500

# After model.save_pretrained_gguf
🔹 Exporting model to GGUF format...
Unsloth: Merging model weights to 16-bit format...
config.json: 100%
 724/724 [00:00<00:00, 25.6kB/s]
Found HuggingFace hub cache directory: /root/.cache/huggingface/hub
model.safetensors.index.json: 
 23.9k/? [00:00<00:00, 817kB/s]
Checking cache directory for required files...
Cache check failed: model-00001-of-00002.safetensors not found in local cache.
Not all required files found in cache. Will proceed with downloading.
Checking cache directory for required files...
Cache check failed: tokenizer.model not found in local cache.
Not all required files found in cache. Will proceed with downloading.
Unsloth: Preparing safetensor model files:   0%|          | 0/2 [00:00<?, ?it/s]
model-00001-of-00002.safetensors: 100%
 4.99G/4.99G [02:12<00:00, 145MB/s]
Unsloth: Preparing safetensor model files:  50%|█████     | 1/2 [02:12<02:12, 132.58s/it]
model-00002-of-00002.safetensors: 100%
 2.65G/2.65G [01:17<00:00, 27.0MB/s]
Unsloth: Preparing safetensor model files: 100%|██████████| 2/2 [03:30<00:00, 105.22s/it]
Unsloth: Merging weights into 16bit: 100%|██████████| 2/2 [03:28<00:00, 104.02s/it]
Unsloth: Merge process complete. Saved to `/content/gguf_model`
Unsloth: Converting to GGUF format...
==((====))==  Unsloth: Conversion from HF to GGUF information
   \\   /|    [0] Installing llama.cpp might take 3 minutes.
O^O/ \_/ \    [1] Converting HF to GGUF f16 might take 3 minutes.
\        /    [2] Converting GGUF f16 to ['q4_k_m'] might take 10 minutes each.
 "-____-"     In total, you will have to wait at least 16 minutes.

Unsloth: Installing llama.cpp. This might take 3 minutes...
Unsloth: Updating system package directories
Unsloth: All required system packages already installed!
Unsloth: Install llama.cpp and building - please wait 1 to 3 minutes
Unsloth: Cloning llama.cpp repository
Unsloth: Install GGUF and other packages
Unsloth: Successfully installed llama.cpp!
Unsloth: Preparing converter script...
Unsloth: [1] Converting model into f16 GGUF format.
This might take 3 minutes...
Unsloth: Initial conversion completed! Files: ['phi-3-mini-4k-instruct.F16.gguf']
Unsloth: [2] Converting GGUF f16 into q4_k_m. This might take 10 minutes...
Unsloth: Model files cleanup...
Unsloth: All GGUF conversions completed successfully!
Generated files: ['phi-3-mini-4k-instruct.Q4_K_M.gguf']
Unsloth: example usage for text only LLMs: llama-cli --model phi-3-mini-4k-instruct.Q4_K_M.gguf -p "why is the sky blue?"
Unsloth: Saved Ollama Modelfile to current directory
Unsloth: convert model to ollama format by running - ollama create model_name -f ./Modelfile - inside current directory.
✅ GGUF model saved successfully in: /content/gguf_model

# After .gguf file is downloaded, need to use it in ollama
llama_model_quantize_impl: model size  =  7288.51 MB
llama_model_quantize_impl: quant size  =  2210.78 MB

# Update this code:
from google.colab import files
import os
gguf_files = [f for f in os.listdir("gguf_model") if f.endswith(".gguf")]
if gguf_files:
    gguf_file = os.path.join("gguf_model", gguf_files[0])
    print(f"Downloading: {gguf_file}")
    files.download(gguf_file)

Once the .gguf file is downloaded to your mac, you need to use a ModelFile

# To download individual files:
from google.colab import files
import os
#files.download("gguf_model/unsloth.F16.gguf")
files.download("gguf_model/unsloth.Q4_K_M.gguf")

OR

from google.colab import files
import os
#files.download("phi-3-mini-4k-instruct.Q4_K_M.gguf")
files.download("phi-3-mini-4k-instruct.Q4_K_M.gguf")

# Note: To see the files, open a terminal in colab
# See that the Q4 version is only 2.2GB
/content/gguf_model# ls -lhr
total 17G
-rw-r--r-- 1 root root 2.2G Aug  2 19:47 unsloth.Q4_K_M.gguf
-rw-r--r-- 1 root root 7.2G Aug  2 19:40 unsloth.F16.gguf
-rw-r--r-- 1 root root 489K Aug  2 19:38 tokenizer.model
-rw-r--r-- 1 root root 3.5M Aug  2 19:33 tokenizer.json
-rw-r--r-- 1 root root 2.9K Aug  2 19:33 tokenizer_config.json
-rw-r--r-- 1 root root  572 Aug  2 19:33 special_tokens_map.json
-rw-r--r-- 1 root root  24K Aug  2 19:36 pytorch_model.bin.index.json
-rw-r--r-- 1 root root 2.5G Aug  2 19:36 pytorch_model-00002-of-00002.bin
-rw-r--r-- 1 root root 4.7G Aug  2 19:35 pytorch_model-00001-of-00002.bin
-rw-r--r-- 1 root root  194 Aug  2 19:33 generation_config.json
-rw-r--r-- 1 root root  696 Aug  2 19:33 config.json
-rw-r--r-- 1 root root  407 Aug  2 19:33 chat_template.jinja
-rw-r--r-- 1 root root  293 Aug  2 19:33 added_tokens.json

# NOTE:
As I didnt want to setup ollama locally, I ran the project:
/Users/gjohnson/Downloads/1_ollama-local-llm-docker
docker exec -it 1_ollama_container ollama run tinyllama
docker exec -it 1_ollama_container ollama list

# Then went back to:
/Users/gjohnson/Downloads/7_fine-tune-llama3-llm-ollama

I updated the Modelfile to find the .gguf file
FROM ./Downloads/unsloth.Q4_K_M.gguf

# To create the model (Ollama on docker remember!)
docker exec -it 1_ollama_container ollama create 7_fine-tune-llama3-llm-ollama-model -f Modelfile

# I was getting this error because the container didnt know about the file!
Graham:7_fine-tune-llama3-llm-ollama gjohnson$ docker exec -it 1_ollama_container ollama create 7_fine-tune-llama3-llm-ollama-model -f Modelfile
Error: no Modelfile or safetensors files found

# So, upload the Modelfile and GGUF file to verify!
docker cp /Users/gjohnson/Downloads/7_fine-tune-llama3-llm-ollama/Modelfile 1_ollama_container:/root/Modelfile
(Successfully copied 2.05kB to 1_ollama_container:/root/Modelfile)

docker cp /Users/gjohnson/Downloads/7_fine-tune-llama3-llm-ollama/unsloth.Q4_K_M.gguf 1_ollama_container:/root/unsloth.Q4_K_M.gguf
OR
docker cp /Users/gjohnson/Downloads/7_fine-tune-llama3-llm-ollama/phi-3-mini-4k-instruct.Q4_K_M.gguf 1_ollama_container:/root/phi-3-mini-4k-instruct.Q4_K_M.gguf
(Successfully copied 2.32GB to 1_ollama_container:/root/phi-3-mini-4k-instruct.Q4_K_M.gguf)

# Check the files are there!
docker exec -it 1_ollama_container ls -lh /root

Graham:7_fine-tune-llama3-llm-ollama gjohnson$ docker exec -it 1_ollama_container ls -lh /root
total 2.2G
-rw-r--r-- 1 501 dialout  287 Oct 23 12:47 Modelfile
-rw-r--r-- 1 501 dialout 2.2G Oct 23 12:43 phi-3-mini-4k-instruct.Q4_K_M.gguf

# As everything went to root in docker, had to use this line in Modelfile:
FROM /root/unsloth.Q4_K_M.gguf

# Create the model!!
docker exec -it 1_ollama_container ollama create 7_fine-tune-llama3-llm-ollama-model -f /root/Modelfile

# Check the model now exists
docker exec -it 1_ollama_container ollama list

# Test the model
docker exec -it 1_ollama_container ollama run 7_fine-tune-llama3-llm-ollama-model:latest

# Send the sample message to the model (from the json data file)
Extract the product information:\n<div class='product'><h2>Asus ROG Strix</h2><span class='price'>$1106</span><span class='category'>electronics</span><span class='brand'>Amazon</span></div>
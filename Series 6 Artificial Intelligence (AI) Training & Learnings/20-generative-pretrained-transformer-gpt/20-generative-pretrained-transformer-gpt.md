# Project 20: Generative Pretrained Transformer
# ---------------------------------------------
# ---------------------------------------------
# Folder:
20_generative-pretrained-transformer-gpt

# Program
Self-contained "baby GPT" in Python for demo.
Its not powerful, but it is a real Transformer that learns to generate text.

# why does the generated text not output all the text ?
Short answer: because the model is not trying to recite the training text — 
it’s trying to predict one token at a time and you’re sampling from its predictions, 
not forcing it to reproduce the full sequence.

# 1. GPTs don’t “store” a string – they learn probabilities
During training, the model sees your text:
hello world. this is a tiny gpt-like model for a demo.

It’s trained to do one thing:
Given some previous characters, predict the next one.

So it learns things like:
after "a tiny gpt-like model for a " → "d" (for “demo”) is very likely
after "demo" → "." is very likely
after "world" → "." is likely
etc.

It never memorizes:
“If I start, I must output this exact string in this exact order.”
Instead it learns:
“Given this context, here are the probabilities of the next character.”

# 2. Generation = rolling the dice, not replaying the script
In your generate method:
probs = F.softmax(logits, dim=-1)
idx_next = torch.multinomial(probs, num_samples=1)
idx = torch.cat((idx, idx_next), dim=1)

torch.multinomial samples from the probability distribution.

That means:
Even if "h" is the most likely next char,
The model might still pick another char with lower probability,
Once it “drifts” slightly, the future predictions also change.

So the model:
Might start generating the training sentence,
Then take a slightly different turn,
Then fall into some loop like:
"a demo. a demo. this is a tiny gpt-like model for a demo."

This is normal, and exactly what “generative” means.

# 3. Context window + sampling = it often loops rather than finishing
You have:
block_size = 16

So the model only sees the last 16 characters at any step during generation.
That means:
It has no guarantee of tracking “where am I in the original full sentence?”
It only knows: “given these last 16 chars, what’s likely next?”
If some 16-character pattern appears multiple times in your training text, 
the model tends to loop around those familiar subsequences, 
rather than walk through the entire training string one time.

# 4. You start from a dummy token, not from the real text
Your generation starts with:
context = torch.zeros((1, 1), dtype=torch.long, device=device)

So the model starts from token 0, which might correspond to some arbitrary character (depending on your vocab ordering), or just be a weird prompt.

You’re not saying:
“Please start by outputting ‘hello world…’ and then continue.”

You’re saying:
“Here is this weird starting token; now make up something likely from there.”
If you want it to continue from a real prefix, you’d do something like:

start = "hello "
context = torch.tensor([encode(start)], dtype=torch.long, device=device)
generated = model.generate(context, max_new_tokens=100)[0].tolist()
print(start + decode(generated[len(start):]))

Even then, it’s still sampling, so it may continue in different ways.

# 5. The model is tiny and the dataset is tiny
Very few parameters (small embed_dim, few layers),
Very little data (one sentence).

So:
It overfits / memorizes style, not robust structure.
It repeats and loops instead of producing a clean “start → end” replay.
For a proper “recitation” of training text, you’d usually:
Train longer,
Use a bigger model,
Use more structured data,
Or force greedy decoding (always pick the most likely char) instead of sampling.

Example (inside generate):
probs = F.softmax(logits, dim=-1)
idx_next = torch.argmax(probs, dim=-1, keepdim=True)  # greedy instead of sampling

Even then, it might not exactly output the full original string, but it will be much more deterministic.

TL;DR for your demo explanation
You can phrase it like this to your audience:

“The model doesn’t store the training sentence and replay it.
It learns the statistics of what character tends to follow what context.
When we generate, we roll the dice at each step based on those learned probabilities.
That’s why it often produces something similar to the training text,
but not necessarily the exact full sentence.”

🧠 Why does increasing block size help?
Because Transformers work by attending over all previous tokens within the block. With larger context, the model learns long patterns like:
How sentences start/end
That “gpt models use attention…” is a complete thought
That newlines separate ideas
Word relationships across longer spans (“attention” → “predict the next token”)

# Install venv
python3.12 -m venv .venv
source .venv/bin/activate

# Training requires torch
pip install torch

# To run the app
python3.12 mini-gpt.py
python3.12 mini-gpt-advanced.py
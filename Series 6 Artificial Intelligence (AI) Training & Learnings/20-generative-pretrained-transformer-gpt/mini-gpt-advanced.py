# Demo-friendly script with:
# a prompt-based generate (no more random zero token),
# a configurable max_new_tokens,
# and multiple sample lengths (100, 300, 600 chars) so you can show the difference live.

import torch
import torch.nn as nn
import torch.nn.functional as F

# =========================
# 0. Config
# =========================
block_size = 64      # context length
embed_dim  = 64
num_heads  = 4
num_layers = 3
num_epochs = 2000
batch_size = 32
learning_rate = 3e-3

device = "cuda" if torch.cuda.is_available() else "cpu"

# =========================
# 1. Training text
# =========================
text = """
hello world. this is a tiny gpt-like model for a demo.
gpt models use attention to predict the next token.
this is a fun experiment!
"""

# Build character-level vocab
chars = sorted(list(set(text)))
vocab_size = len(chars)
stoi = {ch: i for i, ch in enumerate(chars)}
itos = {i: ch for ch, i in stoi.items()}

def encode(s):
    return [stoi[c] for c in s]

def decode(indices):
    return "".join(itos[i] for i in indices)

data = torch.tensor(encode(text), dtype=torch.long)

# =========================
# 2. Dataset helper
# =========================
def get_batch(batch_size):
    # Random chunks of length block_size
    ix = torch.randint(len(data) - block_size, (batch_size,))
    x = torch.stack([data[i : i + block_size] for i in ix])
    y = torch.stack([data[i + 1 : i + block_size + 1] for i in ix])
    return x.to(device), y.to(device)

# =========================
# 3. Tiny GPT-like model
# =========================
class SelfAttentionHead(nn.Module):
    def __init__(self, embed_dim, head_size):
        super().__init__()
        self.key = nn.Linear(embed_dim, head_size, bias=False)
        self.query = nn.Linear(embed_dim, head_size, bias=False)
        self.value = nn.Linear(embed_dim, head_size, bias=False)
        self.register_buffer("tril", torch.tril(torch.ones(block_size, block_size)))

    def forward(self, x):
        B, T, C = x.shape
        k = self.key(x)   # (B, T, head_size)
        q = self.query(x) # (B, T, head_size)

        # attention scores
        wei = q @ k.transpose(-2, -1) * (C ** -0.5)  # (B, T, T)
        wei = wei.masked_fill(self.tril[:T, :T] == 0, float("-inf"))
        wei = F.softmax(wei, dim=-1)

        v = self.value(x)
        out = wei @ v  # (B, T, head_size)
        return out


class MultiHeadAttention(nn.Module):
    def __init__(self, embed_dim, num_heads):
        super().__init__()
        head_size = embed_dim // num_heads
        self.heads = nn.ModuleList(
            [SelfAttentionHead(embed_dim, head_size) for _ in range(num_heads)]
        )
        self.proj = nn.Linear(embed_dim, embed_dim)

    def forward(self, x):
        out = torch.cat([h(x) for h in self.heads], dim=-1)
        out = self.proj(out)
        return out


class FeedForward(nn.Module):
    def __init__(self, embed_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(embed_dim, 4 * embed_dim),
            nn.ReLU(),
            nn.Linear(4 * embed_dim, embed_dim),
        )

    def forward(self, x):
        return self.net(x)


class TransformerBlock(nn.Module):
    def __init__(self, embed_dim, num_heads):
        super().__init__()
        self.ln1 = nn.LayerNorm(embed_dim)
        self.ln2 = nn.LayerNorm(embed_dim)
        self.attn = MultiHeadAttention(embed_dim, num_heads)
        self.ff = FeedForward(embed_dim)

    def forward(self, x):
        x = x + self.attn(self.ln1(x))  # residual
        x = x + self.ff(self.ln2(x))    # residual
        return x


class TinyGPT(nn.Module):
    def __init__(self, vocab_size, embed_dim, block_size, num_heads, num_layers):
        super().__init__()
        self.block_size = block_size
        self.token_emb = nn.Embedding(vocab_size, embed_dim)
        self.pos_emb = nn.Embedding(block_size, embed_dim)
        self.blocks = nn.ModuleList(
            [TransformerBlock(embed_dim, num_heads) for _ in range(num_layers)]
        )
        self.ln_f = nn.LayerNorm(embed_dim)
        self.head = nn.Linear(embed_dim, vocab_size)

    def forward(self, idx, targets=None):
        B, T = idx.shape
        tok_emb = self.token_emb(idx)                         # (B, T, C)
        pos_emb = self.pos_emb(torch.arange(T, device=idx.device))  # (T, C)
        x = tok_emb + pos_emb                                 # (B, T, C)

        for block in self.blocks:
            x = block(x)

        x = self.ln_f(x)
        logits = self.head(x)                                # (B, T, vocab_size)

        if targets is None:
            loss = None
        else:
            B, T, C = logits.shape
            logits = logits.view(B * T, C)
            targets = targets.view(B * T)
            loss = F.cross_entropy(logits, targets)

        return logits, loss

    @torch.no_grad()
    def generate(self, idx, max_new_tokens, temperature=1.0, greedy=False):
        # idx: (B, T)
        for _ in range(max_new_tokens):
            idx_cond = idx[:, -self.block_size:]  # crop to last block_size
            logits, _ = self(idx_cond)
            logits = logits[:, -1, :]  # last time step

            if temperature != 1.0:
                logits = logits / temperature

            if greedy:
                # always take most likely char
                idx_next = torch.argmax(logits, dim=-1, keepdim=True)
            else:
                # sample from distribution
                probs = F.softmax(logits, dim=-1)
                idx_next = torch.multinomial(probs, num_samples=1)

            idx = torch.cat((idx, idx_next), dim=1)
        return idx


# =========================
# 4. Train
# =========================
model = TinyGPT(vocab_size, embed_dim, block_size, num_heads, num_layers).to(device)
optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)

print("Training...")
for step in range(num_epochs):
    x, y = get_batch(batch_size)
    logits, loss = model(x, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if (step + 1) % 200 == 0:
        print(f"step {step+1}/{num_epochs}, loss = {loss.item():.4f}")

# =========================
# 5. Demo generation helper
# =========================
def generate_from_prompt(prompt, max_new_tokens, temperature=1.0, greedy=False):
    model.eval()
    if not prompt:
        # avoid empty prompt edge case
        prompt = "hello "

    # ensure prompt fits in block_size
    encoded = encode(prompt)
    if len(encoded) == 0:
        encoded = [0]
    context = torch.tensor([encoded], dtype=torch.long, device=device)

    with torch.no_grad():
        out = model.generate(context, max_new_tokens=max_new_tokens,
                             temperature=temperature, greedy=greedy)[0].tolist()
    return decode(out)

# =========================
# 6. Show multiple samples
# =========================
print("\n=== DEMO: Sampling (temperature = 1.0) ===")
for length in [100, 300, 600]:
    print(f"\n--- Sample (len={length}) ---")
    print(generate_from_prompt(
        prompt="hello world. ",
        max_new_tokens=length,
        temperature=1.0,
        greedy=False,
    ))

print("\n=== DEMO: Greedy decoding (deterministic) ===")
print(generate_from_prompt(
    prompt="gpt models ",
    max_new_tokens=200,
    temperature=1.0,
    greedy=True,
))
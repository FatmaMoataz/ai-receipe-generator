!fuser -k 8000/tcp
!rm -f cloudflared
!pip install -q transformers accelerate fastapi uvicorn pydantic nest-asyncio requests
!curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o cloudflared
!chmod +x cloudflared

import os
import torch
import re
import json
import asyncio
import subprocess
import nest_asyncio
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer

os.system("pkill cloudflared")

# --- 2. CONFIGURATION & MODEL LOADING ---
model_name = "mistralai/Mistral-7B-Instruct-v0.2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"
)

# --- 3. UTILITY FUNCTIONS ---
def build_prompt(ingredients: str):
    return f"""<s>[INST] Return ONLY a valid JSON object for a recipe using: {ingredients}.
Do not include any text before or after the JSON.
Keep instructions concise to avoid formatting errors.

Structure:
{{
  "recipe_name": "name",
  "time": "mins",
  "calories": 0,
  "cost": "Low",
  "ingredients": [{{ "name": "n", "quantity": "q" }}],
  "instructions": ["step1"]
}} [/INST]"""

def generate_text(prompt, max_new_tokens=600):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=0.2,
        top_p=0.95
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def extract_json(text):
    marker = '"recipe_name"'
    last_occurrence = text.rfind(marker)
    if last_occurrence == -1: return None
    
    start_index = text.rfind('{', 0, last_occurrence)
    end_index = text.rfind('}')
    
    if start_index != -1 and end_index != -1:
        json_content = text[start_index:end_index + 1].strip()
        if not json_content.endswith('}'):
            if json_content.count('[') > json_content.count(']'): json_content += ']'
            json_content += '}'
        return json_content
    return None

# --- 4. FASTAPI SETUP ---
app = FastAPI()

class IngredientsInput(BaseModel):
    ingredients: str

@app.post("/generate")
async def generate(data: IngredientsInput):
    try:
        print(f"🍳 Received request for: {data.ingredients}")
        prompt = build_prompt(data.ingredients)
        output = generate_text(prompt)
        json_str = extract_json(output)
        
        if json_str:
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                # محاولة إصلاح بسيطة للفواصل الناقصة
                fixed_json = re.sub(r'}\s*{', '},{', json_str)
                fixed_json = re.sub(r'"\s+"', '", "', fixed_json)
                return json.loads(fixed_json)
        
        return {"error": "No JSON found", "raw": output}
    except Exception as e:
        print(f"🔥 Error: {str(e)}")
        return {"error": str(e)}

# --- 5. TUNNEL & SERVER RUNNER ---
def start_cloudflare():
    p = subprocess.Popen(["./cloudflared", "tunnel", "--url", "http://127.0.0.1:8000"], 
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    print("⏳ Establishing Cloudflare Tunnel...")
    for _ in range(50):
        line = p.stdout.readline()
        if "trycloudflare.com" in line:
            url = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
            if url:
                print("\n" + "="*40)
                print("🚀 API IS LIVE!")
                print(f"URL: {url.group(0)}/generate")
                print("="*40 + "\n")
                return url.group(0)
    return None

nest_asyncio.apply()

async def run_server():
    config = uvicorn.Config(app, host="127.0.0.1", port=8000, loop="asyncio")
    server = uvicorn.Server(config)
    await server.serve()

# --- 6. EXECUTION ---
tunnel_url = start_cloudflare()
if tunnel_url:
    loop = asyncio.get_event_loop()
    loop.create_task(run_server())

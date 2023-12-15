import os
import openai
from fastapi import FastAPI
import json
import requests
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Setting the API key
openai.api_key = os.getenv('OPENAI_API_KEY')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Prompt(BaseModel):
    prompt: str

class SummarizeSchema(BaseModel):
    prompt: str
    inst: str

def Gpt_API(prompt, instruction):
    completion = openai.ChatCompletion.create(
    # Use GPT 3.5 as the LLM
    model="gpt-3.5-turbo",
    # Pre-define conversation messages for the possible roles
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": instruction}
    ]
    )
    # Print the returned output from the LLM model
    answer = completion.choices[0].message.content
    print(answer)

    return answer

class GenerateContentSchema(BaseModel):
    prompt: str
    length: str
    typeof: str

@app.post("/api/shorten")
async def shorten(info: Prompt):
    prompt = info.prompt

    
    return prompt


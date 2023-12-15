import os
import openai
from fastapi import FastAPI
import json

from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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



@app.post("/api/shorten")
async def shorten(info: Prompt):
    prompt = info.prompt

    
    return prompt


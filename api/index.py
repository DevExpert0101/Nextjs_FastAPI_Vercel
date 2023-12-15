import os
import requests
from fastapi import FastAPI
import json
import openai
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
    instruction = ''''Shorten if the above sentence in the paragraph is larger.    If so, suggest a shorter sentence. Please output only shorten senences and json format like this:'
   
        {
            "sentence":    "The research on    our    universe is    still    ongoing
                on    scientists    are constantly    discovering new    facts    and learning
                more about    our    galaxy    and beyond."
        }
        or
        {
            "sentences":    [
                "The research on    our    universe is    ongoing and scientists
                are constantly    learning more about    it.",
                "Scientists    are constantly    learning more about    our
                universe."
            ]
        }
        '''
   
    return prompt


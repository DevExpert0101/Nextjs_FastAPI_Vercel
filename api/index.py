import os
import openai
from fastapi import FastAPI
import json
import requests
from pydantic import BaseModel

app = FastAPI()

# Setting the API key
openai.api_key = os.getenv('OPENAI_API_KEY')


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

@app.post("/api/generate_content")
async def Generate_Content(info: GenerateContentSchema):
    # Define the user prompt message
    prompt = info.prompt
    length = info.length
    typeof = info.typeof
    # Create a chatbot using ChatCompletion.create() function
    
    instruction = ''
    if typeof == 'table':
        instruction = f'Generate table and content in bullet points. The length should be {length} and output the source of the generated data or content. e.g. wikipedia, etc.'
    elif typeof == 'content':
        instruction = f'Generate content for above.The length should be {length} and output the source of the generated data or content. e.g. wikipedia, etc.'
    elif typeof == 'withimages':
        instruction = f'Generate content and images for above. The length should be {length} and output the source of the generated data or content. e.g. wikipedia, etc.'
    
    rlt = Gpt_API(prompt, instruction)

    data = {
        'contentgen': rlt,        
    }

    return data

@app.post("/api/correct_grammar")
async def Correct_Grammar(info: Prompt):
    # prompt = info.prompt
    prompt = "You are a grammar assistant."
    instruction = info.prompt + '''Please correct grammar from above sentences. The output should be the report of check result and like this format:
        Compare original sentences and corrected sentences and give me output like this:                            
    {
        iscorrect: false,
        correction: [{
            "action": "", // replace, update, delete
            "wordPosition": "",
            "word": ""
        }, {
            "action": "", // replace, update, delete
            "wordPosition": "",
            "word": ""
        }
        ]
    }'''
    rlt = Gpt_API(prompt, instruction)
    return json.loads(rlt)

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
    rlt = Gpt_API(prompt, instruction)
    data = json.loads(rlt)
    
    return data

@app.post("/api/toactivevoice")
async def Fix_Sentence(info: Prompt):
    prompt = info.prompt
    instruction = prompt + '''If above is passive voice then fix adverb and passive voice into active.
                Output should be json format like this:
                {
                    isactivevoice: , // If above sentence is active then true, else false
                    correctSentence: ""
                }
                '''
    rlt = Gpt_API(prompt, instruction)
    return json.loads(rlt)

@app.post("/api/summarize")
async def Summarize(info: Prompt):
    prompt = info.prompt    
    instruction = 'Summarize the above sentence or the whole document.'
    rlt = Gpt_API(prompt, instruction)
    json
    return { 'content': rlt}

@app.post("/api/suggestions")
async def Suggestions(info: Prompt):
    prompt = info.prompt
    instruction = '''Generate multiple suggestions for an incomplete sentence or the next line for above.
                    Output shuold be json format like this:
                    {
                        data: [
                            suggestion 1,
                            suggestion 2,
                        ]
                    }'''
    rlt = Gpt_API(prompt, instruction)
    return json.loads(rlt)

@app.post("/api/generate_image")
async def Generate_Image(info: Prompt):
    prompt = info.prompt
    url = "https://stablediffusionapi.com/api/v3/text2img"

    payload = json.dumps({
    "key": "exu3fsyKu3L8B8lgbvNA5JJulr8akF9epMTrKt6ztKnZui5IFudPJjmQsepq",
    "prompt": prompt,
    "negative_prompt": None,
    "width": "512",
    "height": "512",
    "samples": "1",
    "num_inference_steps": "20",
    "seed": None,
    "guidance_scale": 7.5,
    "safety_checker": "yes",
    "multi_lingual": "no",
    "panorama": "no",
    "self_attention": "no",
    "upscale": "no",
    "embeddings_model": None,
    "webhook": None,
    "track_id": None
    })

    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.json())
    data = response.json()
    return data['output']

class ContentGenRequestSchema(BaseModel):
    longessay: str
    question: str
    action: str

@app.post("/api/contentAnsGen")
async def ContentAndGen(request: ContentGenRequestSchema):
    prompt = "You are a assistant."

    instruction = request.longessay + request.question
    rlt = Gpt_API(prompt, instruction)
    return { "sentence" : rlt }
    

@app.post("/api/expand")
async def expand(request: Prompt):
    prompt = request.prompt
    instruction = "Please expand above sentence."
    rlt = Gpt_API(prompt, instruction)
    return { "sentence": rlt}

class RewriteSchema(BaseModel):
    sentence: str
    tone: str
    
@app.post("/api/rewrite")
async def rewrite(request: RewriteSchema):
    prompt = request.sentence
    instruction = '''Please rewrite above sentence as {request.tone} tone.
                    Output should be like this:
                    {
                        "sentences":    [
                            "The research on    our    universe is    ongoing and scientists
                            are constantly    learning more about    it.",
                            "Scientists    are constantly    learning more about    our
                            universe."
                        ]
                    }'''
    rlt = Gpt_API(prompt, instruction)
    
    return json.loads(rlt)


@app.post("/api/fix-adverb")
async def fix_adverb(request: Prompt):
    prompt = request.prompt
    instruction = 'Please fix adverbs in above sentences.'
    rlt =  Gpt_API(prompt, instruction)

    return { "sentence" : rlt }

@app.post("/api/readable")
async def readable(request: Prompt):
    prompt = request.prompt
    instruction = 'Please replace complex words into simple alterantive in above sentence.'
    rlt = Gpt_API(prompt, instruction)

    return { "sentence" : rlt }

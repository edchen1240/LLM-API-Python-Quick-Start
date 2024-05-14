"""
[OpenAi-API-0_FuncBank.py]
Purpose: Correct Ask Directory or select file.
Author: Meng-Chi Ed Chen
Date: 2023-07-07
Updates:
    1. 2024-03-11: Upgrade interation question to allow new topic, follow up, or the original select file.
    2.

Status: Complete.
"""

import sys, os, base64, tkinter, datetime, json, requests, subprocess, re, shutil, time
from tkinter import filedialog
from openai import OpenAI
from datetime import datetime, timedelta
import LLM_00_module_2_Peripheral as PERF #type: ignore


def check_API_key(api_key):
    if api_key is None or api_key == 'put-your-api-key-here':
        raise ValueError('--API key not provided. Please put your API key at "put-your-api-key-here" in the code.')
    return api_key


#[1] OpenAI API functions

#[1-1] Ask text question. Used most frequent.
def OpenAI_GPT_API_short(model_name, openai_api_key, question_content, temperature):
    print('\n[OpenAI_GPT_API_short]')
    #[1] Check API key and attach it.
    check_API_key(openai_api_key)
    openai_api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    messages = [{'role': 'user', 'content': question_content}]
    
    # [3] Check if this is a vision problem.
    if 'vision' in model_name.lower() or 'o' in model_name.lower():
        text = 'This is a vision model. Choose an image for this vision question.'
        print(text)
        path_image, basename_image = PERF.tkinter_select_file(dialog_title = text)
        if path_image:
            base64_image = encode_image(path_image)
            messages.append({
                'role': 'user',
                'content': [{
                    'type': 'image_url',
                    'image_url': {
                        'url': f"data:image/jpeg;base64,{base64_image}"
                    }
                }]
            })
    
    #[5] Set model name and temperature
    data = {
        "model": model_name,
        "messages": messages,
        "temperature": temperature
    }

    print('--Sending API request. Please wait for HTTP request-response cycle.\n')
    response = requests.post(openai_api_url, headers=headers, json=data)
    
    #[6] Organize response
    content = None
    if response.status_code == 200:
        response_data = response.json()
        content = response_data["choices"][0]["message"]["content"]
        usage_prompt = str(response_data["usage"]["prompt_tokens"])
        usage_completion = str(response_data["usage"]["completion_tokens"])
        usage_total = str(response_data["usage"]["total_tokens"])
        info_2nd_row = f'[Model]{model_name} [Token](input, output): {usage_prompt}, {usage_completion}.'
        content = info_2nd_row + '\n\n' + content + '\n'
    else:
        print("Error:", response.status_code, response.text, sep='\n')
    return content



#[1-2] Ask text question. Use this if you prefer to include additional_info such as timestamp and token usage.
def OpenAI_GPT_API_long(model_name, openai_api_key, question_content, temperature, additional_info=0):
    print('\n[OpenAI_GPT_API_long]')
    t0 = time.time()
    check_API_key(openai_api_key)
    # API portle and header for autherization.
    openai_api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }
    data = {
        "model": model_name,
        "messages": [{'role': 'user', 'content': question_content}],
        #"role" can be "system"(provide instructions or contextual information to the AI model) 
        # or "user"(normal human asking questions).
        "temperature": temperature 
        #"temperature" is the randomness of the response. 0 is very deterministic and 1 is very creative.
    }
    #[] Send the POST request to the OpenAI API
    print('--Sending API request. Please wait for HTTP request-response cycle.\n')    
    response = requests.post(openai_api_url, headers=headers, data=json.dumps(data))
    t1 = time.time()
    time_span = round(t1-t0,2)
    if response.status_code == 200:
        #[Dictionary] response_data were stored in a format of python dictionary with multiple "key:value" pairs.
        response_data = response.json() 
        content = response_data["choices"][0]["message"]["content"]
        if additional_info == 1:
            info_created = str(datetime.utcfromtimestamp(response_data["created"]))
            info_model = str(response_data["model"])
            usage_prompt = str(response_data["usage"]["prompt_tokens"])
            usage_completion = str(response_data["usage"]["completion_tokens"])
            usage_total = str(response_data["usage"]["total_tokens"])
            #[] Combine text (Change this part if you prefer other reporting format.)
            info_1st_row = f'[Info] (model, timestamp, time span): {info_model}, {info_created}, {time_span}.' 
            info_2nd_row = f'[Token] {model_name} (prompt, completion, total): {usage_prompt}, {usage_completion}, {usage_total}.'
            content = info_1st_row + '\n' + info_2nd_row + '\n\n' + content + '\n'
        print('[Response preview]\n', str(content)[:200])
    else:
        print("Error:", response.status_code, response.text, sep='\n')
    return content
    
def encode_image(image_path):
    # Check if the file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"The file {image_path} does not exist.")
    # Extract the file extension
    _, file_extension = os.path.splitext(image_path)
    # Define acceptable image formats
    acceptable_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
    # Check if the file is an acceptable image format
    if file_extension.lower() not in acceptable_formats:
        raise ValueError(f"Unsupported file format: {file_extension}. Please use one of the following formats: {', '.join(acceptable_formats)}")
    # If the file format is acceptable, proceed with encoding
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

#[1-3] Ask text and image question.
def OpenAI_GPT_API_image_path(model_name, openai_api_key, question_content, path_image, additional_info):
    print('\n[OpenAI_GPT_API_image_path]')
    check_API_key(openai_api_key)
    base64_image = encode_image(path_image)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }
    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question_content},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                    }
                ]
            }
        ],
        "max_tokens": 500
    }
    #[] Send the POST request to the OpenAI API
    print('--Sending API request. Please wait for HTTP request-response cycle.\n')
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    if response.status_code == 200:
        response_data = response.json()
        content = response_data["choices"][0]["message"]["content"]
        if additional_info == 1:
            info_id = str(response_data["id"])
            info_object = str(response_data["object"])
            info_created = str(datetime.utcfromtimestamp(response_data["created"]))
            info_model = str(response_data["model"])
            usage_prompt = str(response_data["usage"]["prompt_tokens"])
            usage_completion = str(response_data["usage"]["completion_tokens"])
            usage_total = str(response_data["usage"]["total_tokens"])
            #[] Combine text
            info_1st_row = f'[Info] (ID, Object, Timestamp, Model): {info_id}, {info_object}, {info_created}, {info_model}.' 
            info_2nd_row = f'[Token] {model_name} (prompt, completion, total): {usage_prompt}, {usage_completion}, {usage_total}.'
            content = info_1st_row + '\n' + info_2nd_row + '\n\n' + content + '\n'
    else:
        print("Error:", response.status_code, response.text, sep='\n')
        content = None

    return content



#[2] Gemini API functions

import google.generativeai as genai

def DeepMind_Gemini_API_short(model_name, gemini_api_key, question_content, temperature, max_output_tokens):
    print('\n[Gemini_API_short]')
    check_API_key(gemini_api_key)
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel(model_name)
    #[] Send the POST request to the OpenAI API
    print('--Sending API request. Please wait for HTTP request-response cycle.\n')
    response = model.generate_content(question_content
                                      , generation_config={'temperature': temperature
                                                           ,'max_output_tokens': max_output_tokens})
    content = response.text
    len_input = len(question_content.split(' '))
    len_output = len(content.split(' '))
    info_2nd_row = f'[Model]{model_name} [Token](input, output): {len_input}, {len_output}.'
    content = info_2nd_row + '\n\n' + content + '\n'
    #print(f'\n[response start]\n\n{response}\n\n[response end]\n')
    return content




#[3] Anthropic API functions
import anthropic

def Anthropic_Claude_API_long(model_name, anthropic_api_key, question_content, max_tokens, temperature=None):
    print('\n[Anthropic_Claude_API_long]')
    check_API_key(anthropic_api_key)
    anthropic_api_url = 'https://api.anthropic.com/v1/messages'
    headers = {"Content-Type": "application/json",
                "x-api-key": anthropic_api_key, 
                "anthropic-version": "2023-06-01"}
    data = {"model": model_name,
            "max_tokens": max_tokens,
            "messages": [{'role': 'user', 'content': question_content}]}
    if temperature is not None:
        data["temperature"] = temperature
    print('--Sending API request. Please wait for HTTP request-response cycle.\n')
    response = requests.post(anthropic_api_url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response_data = response.json()
        texts = [message["text"] for message in response_data["content"]]
        content = "\n".join(texts)
        usage_input = str(response_data["usage"]["input_tokens"])
        usage_output = str(response_data["usage"]["output_tokens"])
        info_2nd_row = f'[Model]{model_name} [Token](input, output): {usage_input}, {usage_output}.'
        content = info_2nd_row + '\n\n' + content + '\n'
    else:
        print("Error:", response.status_code, response.text, sep='\n')
        content = None
    return content


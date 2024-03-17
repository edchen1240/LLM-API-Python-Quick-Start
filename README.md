# LLM API Python Quick Start

Welcome to the API Python Quick Start Guide for large language models (LLM). This repository includes working basic API functions to connect to ChatGPT by OpenAI, Gemini by Google Deepmind, and Claude by Anthropic. Ideal for beginners in coding or for those seeking to streamline their initial exploration. :blush:

## Introduction
If a webpage is an interface designed for humans, then an API (Application Programming Interface) is an interface designed for programs. It allows programmers to integrate the web-based OpenAI service into their own applications without unnecessary web scrapping.
### Pros of using the API to access ChatGPT:
- Gain access to potentially newer models and exclusive features not available on the standard web interface.
- Enhanced privacy for your interactions.
- Enables the integration of LLM's capabilities into your custom applications.
- Avoid congestion on webpage service.
- Bypass organizational internet censorship to LLMs.
### Cons of using the API to access ChatGPT:
- Python installation on your computer is require, or other method that have access to API.
- Involves a small amount of programming (reading a few lines of code, modifying something, and debugging if necessary).
- It's not free. (API for )
i. ChatGPT by OpenAI is not free, and it required a payment method (e.g. credit card).
ii. Gemini by Google DeepMind and Claude by Anthropic are currently free (2024-03-16).
&nbsp;

## File Contents
### General
- `LLM_00_module_1_API.py`:
    Store API related functions that connects to different LLM.
- `LLM_00_module_2_Peripheral.py`:
    Store other functions that makes the automation works.
### OpenAI
- `LLM_01_OpenAI_1_text.py`:
    Code for submitting text queries from a .txt file to ChatGPT.
- `LLM_01_OpenAI_2_text+image.py`:
    Code for submitting text queries from a .txt file to ChatGPT and an image file (formats: .jpg, .jpeg, .png, .bmp, or .gif).
- `LLM_01_OpenAI_3_autoText.py`:
    Code for submitting text to ChatGPT with upgrade interation question to allow (a) new topic, (b) follow up, or the original (c) select file.
### Google DeepMind
- `LLM_02_Gemini_1_text.py`:
    Code for submitting text queries from a .txt file to Gemini.
- `LLM_02_Gemini_3_autoText.py`:
    Code for submitting text to Gemini with upgrade interation question to allow (a) new topic, (b) follow up, or the original (c) select file.
### Anthropic
- `LLM_03_Claude_1_text.py`:
    Code for submitting text queries from a .txt file to Gemini.
- `LLM_03_Claude_3_autoText.py`:
    Code for submitting text to Gemini with upgrade interation question to allow (a) new topic, (b) follow up, or the original (c) select file.

## Requirement
1. Make sure your organization allows you to visit [this webpage](https://github.com/edchen1240/OpenAI-API-Python-Quick-Start) that you are currently looking at, and the API portal of these LLM providers:
    1. OpenAI: [https://api.openai.com/](https://api.openai.com/). (Should be able to see a welcome message.)
    2. Google DeepMind: The library `google.generativeai` handles the URL that connects to the APL protal.
    3. Anthropic: [https://api.anthropic.com/v1/messages](https://api.anthropic.com/v1/messages). (Should be able to see "method not allowed".)
2. Install python and an IDE (like [VSCode](https://code.visualstudio.com/docs/python/python-tutorial)), as well as necessary libraries in OpenAI_API_0_module\.py. (Such as sys, os, base64, tkinter, datetime, json, requests, subprocess, re, and shutil.)
3. Sign-up for API keys at each LLM providor's website. For ChatGPT, acquire OpenAI API key at [OpenAI's official website](https://openai.com/blog/openai-api). (Might need a credit or debit card as payment method.)


## Steps for Running with an IDE
We recommend following these steps if you're running the code for the first time:
1. Download the Python files into the same folder.
2. Create a .txt file with questions somewhere on your computer.
3. Run `OpenAI_API_1_text.py` and select the question file in the pop-up dialogue.
   (If running `OpenAI_API_2_text+image`, the first dialogue will ask for the text file, and the second will ask for the image file.)
4. If the code previews a portion of the question and pauses for a few seconds, it indicates that it's working and OpenAI is generating a response.
5. Once "Complete" appears, the response has been retrieved, appended to the original question, and saved. You can now open the file to review the response.

## Create a .bat File to Run Without an IDE
1. Create a new text file with a clear name, such as "RUN_CHATGPT.bat", and insert the following code:
```
@echo off
cd /d D:\path\to\your\folder
python OpenAI_API_1_text.py
pause
```
The `OpenAI_API_1_text.py` can be replaced with other files (but not `OpenAI_API_0_module.py`).
2. Save the file and change its extension from .txt to .bat.
3. Double-click "RUN_CHATGPT.bat" to execute the code.

## Note
1. It's an everychanging world, and I might not be able to followup with the major changes. Please refer to OpenAI's website for latest information.
2. Suggestions and recommendations are welcome: [edchen93\@mit.edu](mailto:edchen93@mit.edu)

## Maintaince Record
1. 2024-03-16. First edition upload.

"""
[OpenAI-API-1_text.py]
Purpose: Correct Ask Directory or select file.
Author: Meng-Chi Ed Chen
Date: 2023-11-07
Reference:
    1. 
    2.

Status: Complete.
"""

#[1] Import library.
import LLM_00_module_1_API as APIS #type: ignore
import LLM_00_module_2_Peripheral as PERF #type: ignore
gemini_api_key = 'put-your-api-key-here'  #  put-your-api-key-here.

#[2] Assign model. View more model and pricing here: https://openai.com/pricing
model_name = 'gemini-1.0-pro-latest'	
#model_name = 'gemini-1.0-pro'
#model_name = 'gemini-1.0-pro-001'

#[3] Read question from txt file.
path_txt, basename_text = PERF.tkinter_select_file(dialog_title = 'Choose a question file')
question_content = PERF.read_text_from_txt(path_txt = path_txt, 
                                            char_preview = 300)

#[4] Send API request.
reply = APIS.DeepMind_Gemini_API_short(model_name = model_name
                            , gemini_api_key = gemini_api_key
                            , question_content = question_content
                            , temperature = 0.9
                            , max_output_tokens = 5000)

PERF.append_text_to_txt(path_txt = path_txt
                         , text_to_append = reply
                         , char_preview = 300)
print('[Complete]')
PERF.open_txt(path_txt)

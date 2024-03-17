"""
[OpenAI-API-2_text+image.py]
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
openai_api_key = 'put-your-api-key-here'  #  put-your-api-key-here.

#[2] Assign model. View more model and pricing here: https://openai.com/pricing
model_name = 'gpt-4-vision-preview'

#[2] Read question from txt file
path_txt, basename_txt = PERF.tkinter_select_file(dialog_title = 'Choose a question .txt file')
question_content = PERF.read_text_from_txt(path_txt, 300)
path_image, basename_image = PERF.tkinter_select_file(dialog_title = 'Choose a image file')

#[4] Send API request.
reply = APIS.OpenAI_GPT_API_image_path(model_name
                                        , openai_api_key
                                        , question_content
                                        , path_image
                                        , additional_info=1)
PERF.append_text_to_txt(path_txt, reply, 300)
print('[Complete]')
PERF.open_txt(path_txt)



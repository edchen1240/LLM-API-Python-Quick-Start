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
openai_api_key = 'put-your-api-key-here'  #  put-your-api-key-here.
path_prompt = r'D:\01_Floor\a_Ed\09_EECS\10_Python\03_MatureTools\[LLM API]\01_Codes\09_Common Prompts.txt'
dir_questions = r'D:\01_Floor\a_Ed\09_EECS\10_Python\03_MatureTools\[LLM API]'
PERF.remove_older_asked_questions(dir_questions, 'txt', '00_Asked questions', day=5)
max_loop = 10 # The program will run for 10 times before we need to start it again.


#[2] Assign model. View more model and pricing here: https://openai.com/pricing
model_name = 'gpt-4-0125-preview'	
#model_name = 'gpt-4-1106-preview'
#model_name = "gpt-3.5-turbo"
print(f'[Model] {model_name}')

for loop in range(1, max_loop + 1):
    print(f'[Question Round {loop}]')
    path_txt = PERF.q1_new_file_or_followup(dir_questions, model_name, path_prompt)
    #[2] Read question from txt file.
    question_content = PERF.read_text_from_txt(path_txt = path_txt, 
                                                char_preview = 300)
    #[4] Send API request.
    reply = APIS.OpenAI_GPT_API_short(model_name = model_name
                                    , openai_api_key = openai_api_key
                                    , question_content = question_content
                                    , temperature = 0.9)
    PERF.append_text_to_txt(path_txt = path_txt
                            , text_to_append = reply
                            , char_preview = 300)
    print('[Complete]')
    PERF.open_txt(path_txt)




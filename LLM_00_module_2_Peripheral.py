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






#[1] Basic functions.




def datetime_stamp():
    now = datetime.now()
    return now.strftime("%Y-%m-%d_%H-%M-%S")


def datetime_filename():
    now = datetime.now()
    return now.strftime("%Y-%m%d-%H%M")



#[2] Cool interaction questions.



def q1_new_file_or_followup(dir_questions, model_name, path_prompt=None):
    """
    [Opening question]
    """
    dt_file = datetime_filename()
    message = \
    f'\nHello, how can I help you?   {dt_file}  {model_name}\n\
    (a) Type a new name for the new topic. \n\
        This will create and open a new txt file named as "{dt_file}_Topic-1".\n\
    (b) Type "+" to followup with the latest question.\n\
        This will copy the latest txt file and create a "_n+1" version for it.\n\
    (c) Type nothing (just press enter) to choose an existing text file.\n'
    string_ques = input(message)
    if string_ques == '+':
        path_latest_txt = find_latest_txt(dir_questions)
        path_txt = increment_filename(path_latest_txt)
        basename_txt = os.path.basename(path_txt)
        print(f'--> (b) Followup the latest question: {basename_txt}')
        open_txt(path_txt)
        q2_let_me_know_when_question_is_ready(path_txt, path_prompt)
    elif string_ques == '':
        print('--> (c) Choose an existing question file.')
        path_txt, _ = tkinter_select_file(dialog_title = 'Choose an existing question file')
    else:
        print(f"--> (a) Let's start a new topic of {string_ques}.")
        filename = dt_file + '_' + string_ques + '_1.txt'
        path_txt = create_txt_file(filename, dir_questions)
        open_txt(path_txt)
        q2_let_me_know_when_question_is_ready(path_txt, path_prompt)
    return path_txt



def q2_let_me_know_when_question_is_ready(path_txt="", path_prompt=None):
    print('\n[q2_let_me_know_when_question_is_ready]')
    #print(f'[path_prompt]: {path_prompt}. Is the path_prompt Noen? empty?{path_prompt is not None}  {path_prompt != ""} ')
    basename_txt = os.path.basename(path_txt)
    message = f"The file {basename_txt} has been created and is now open for you.\n"
    
    # Check if path_prompt is not None
    if path_prompt is not None and path_prompt != "":
        basename_prompt = os.path.basename(path_prompt)
        prompt_text = f"\n{read_text_from_txt(path_prompt, char_preview=0)}\n"
        message += f"Here are some common prompts from {basename_prompt} that you might want to use.\n{prompt_text}"
    
    message += "Please save and close the program once you finish compiling the question.\nPress Enter to continue.\n"
    _ = input(message)  # The line is used to wait for enter pressed. Do not delete.
    print("The question is ready. Let's proceed.")



#[3] Peripheral functions

def remove_older_asked_questions(dir_questions, ext, name_dump_folder, day=7):
    print('\n[remove_older_asked_questions]')
    #dir_folder = os.path.dirname(os.path.abspath(__file__))    # Get current directory.
    dir_questions = dir_questions                      # Get directory from path_txt.
    list_file_paths = [os.path.join(dir_questions, file) for file in os.listdir(dir_questions) if file.endswith(ext)]
    dir_dump = os.path.join(dir_questions, name_dump_folder)
    if not os.path.exists(dir_dump):
        os.makedirs(dir_dump)
    cnt_ext_file = len(list_file_paths)
    print(f'--There are {cnt_ext_file} files with extension {ext}.')
    if cnt_ext_file > 5:
        #[3] Sort the files by date
        file_date_map = {}
        for file_path in list_file_paths:
            file_date = os.path.getmtime(file_path)
            file_date_map[file_path] = datetime.fromtimestamp(file_date)
        sorted_files = sorted(file_date_map.items(), key=lambda x: x[1])
        if cnt_ext_file > 20:
            # Remove the oldest (cnt_ext_file - 10) files
            num_files_to_remove = cnt_ext_file - 10
            for i in range(num_files_to_remove):
                file_path, _ = sorted_files[i]
                shutil.move(file_path, dir_dump)
                print(f'--File removed: {os.path.basename(file_path)}')
        else:
            #[5] Remove files older than 'day' days
            current_date = datetime.now()
            for file_path, file_date in sorted_files:
                if current_date - file_date > timedelta(days=day):
                    shutil.move(file_path, dir_dump)
                    print(f'--File removed: {os.path.basename(file_path)}')
    # Get the size of a single directory dir_dump
    dump_size_kB = round(get_directory_size(dir_dump)/1024)
    print(f'--Current size of the dump folder {name_dump_folder} in kB: {dump_size_kB}.\n\n')
    

def get_directory_size(directory):
    total_size = 0
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size



def filter_file_with_keywords(
    dir_folder, 
    list_keywords_select=None, 
    list_keywords_discard=None
    ):
    print('\n[filter_file_with_keywords]')
    if list_keywords_select is None:
        list_keywords_select = []
    if list_keywords_discard is None:
        list_keywords_discard = []
    # Check if directory exists
    if not os.path.isdir(dir_folder):
        raise FileNotFoundError(f"The directory '{dir_folder}' was not found.")
        sys.exit(1)
    # Get list of files in the directory
    list_file_names = [file for file in os.listdir(dir_folder)
                       if os.path.isfile(os.path.join(dir_folder, file))]
    # Filter names by keywords to select
    if list_keywords_select:
        list_file_names = [file for file in list_file_names 
                           if any(keyword in file for keyword in list_keywords_select)]
    # Filter names by keywords to discard
    if list_keywords_discard:
        list_file_names = [file for file in list_file_names 
                           if not any(keyword in file for keyword in list_keywords_discard)]
    # Generate file paths
    list_file_paths = [os.path.join(dir_folder, file) for file in list_file_names]
    # Print result
    print('--list_file_names:', list_file_names, end='\n\n')
    return list_file_paths, list_file_names






def find_latest_txt(dir=None):
    print('\n[find_latest_txt]')
    if dir is None:
        dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(dir, exist_ok=True)  # Ensure the directory exists.
    # Assuming filter_file_with_keywords returns a tuple of (list_of_full_paths, list_of_filenames)
    list_file_paths, list_file_names = filter_file_with_keywords(dir, list_keywords_select='.txt')
    # Now work with the full paths directly
    # Sort full paths by creation time, newest first
    list_file_paths.sort(key=lambda file_path: os.path.getctime(file_path), reverse=True)
    # Check if there are any .txt files
    if list_file_paths:
        # Get the most recently created file's path
        path_latest_txt = list_file_paths[0]  # Take the first element as it's the newest.
        print('--Latest .txt file: ', os.path.basename(path_latest_txt))
    else:
        print('--No .txt files found. Program exit.')
        path_latest_txt = None
        sys.esit()
    return path_latest_txt
    
    
    
    
def increment_filename(path_txt):
    """
    Increments the numerical part of a filename before the '.txt' extension.
    If the file is named 'example_1.txt', it will be changed to 'example_2.txt'.
    If no numerical part is found, '_1' will be added before the extension.
    Save a new cope of path_txt with a new filename in the same dir.
    """
    print('\n[increment_filename]')
    # Regular expression to find the "_{n}.txt" part of the filename
    pattern = re.compile(r"(_(\d+))\.txt$")
    # Search for the pattern in the filename
    match = pattern.search(path_txt)
    if match:
        # Extract the full matched pattern (_{n}) and the numerical part ({n})
        full_match, num_part = match.groups()
        # Increment the number
        num_incremented = int(num_part) + 1
        # Replace the original numerical part with the incremented value
        path_new_txt = path_txt.replace(full_match, f"_{num_incremented}")
    else:
        # If no numerical part is found, add '_1' before the '.txt' extension
        path_new_txt = path_txt.replace(".txt", "_1.txt")
    shutil.copy(path_txt, path_new_txt)
    print(f'--File created at: {path_new_txt}')
    return path_new_txt



def create_txt_file(path_txt, dir=None):
    """
    Create an empty .txt file at the specified directory (or in the current directory if not specified).
    Then open the txt file with the default system application for .txt files, and return the path to that file.
    """
    print('\n[create_txt_file]')
    if dir is None:
        dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(dir, exist_ok=True)  # Ensure the directory exists.
    path_txt = os.path.join(dir, path_txt)  # Create the full path for the file.
    # Create the file if it doesn't exist.
    with open(path_txt, 'w') as file:
        pass  # Just create the file, no need to write anything.
    print(f'--File created at: {path_txt}')
    return path_txt
    
    
    
def open_txt(path_txt):
    print('\n[open_txt]')
    # Open the file with the default application.
    if os.name == 'nt':             # For Windows
        os.startfile(path_txt)
    elif os.name == 'posix':        # For MacOS
        subprocess.run(['open', path_txt])
    else:                           # For Linux (xdg-open should work for most environments)
        subprocess.run(['xdg-open', path_txt])
    return path_txt




def tkinter_select_file(dialog_title='Select a file'):
    print('\n[tkinter_select_file]')
    root = tkinter.Tk() # Creat a window (or container) for tkinter GUI (Graphical User Interface) toolkit
    root.withdraw() # Hide the main window since we don't need to see it.
    try:
        file_path = filedialog.askopenfilename(title=dialog_title)
        if file_path:
            file_basename = os.path.basename(file_path)
            file_path = os.path.normpath(file_path) # Clean the path
            print('--file_path:', file_path)
            return file_path, file_basename
        else:
            print('--No file selected. Exit code.')
            sys.exit()
    except Exception as e:
        print(f'--An error occurred: {e}')
        return None, None
    finally:
        root.destroy() # Release resources.


#[4] Reading, saving, and handling txt files.

#[4-1] Read question from .txt file.
def read_text_from_txt(path_txt, char_preview=0):
    time.sleep(0.5)
    try:
        with open(path_txt, 'r') as file:
            content = file.read()
            if char_preview > 0:
                print('[read_text_from_txt] content quick view:\n >>', content[:char_preview].replace('\n', '\n >> '), '\n')
        return content
    except FileNotFoundError:
        print(f'--File not found:\n {path_txt}')
        sys.exit()
    except Exception as e:
        print(f'--An error occurred while reading the file:\n {str(e)}')
        sys.exit()


#[4-2] Append reply to .txt file and save.
def append_text_to_txt(path_txt, text_to_append, char_preview): # This code will not rename the file.
    #[] Check if the path_txt exists
    if not os.path.exists(path_txt):
        print(f'[append_text_to_txt] File not found:\n {path_txt}')
        sys.exit()
    #[] Get current datetime and create opening_of_append.
    current_datetime = datetime_stamp()
    opening_of_append = '\n\n--\n[' + current_datetime + ']\n'
    try:
        with open(path_txt, 'a') as file:  #a = append, w = write
            file.write(opening_of_append)
            file.write(text_to_append)
            print('[append_text_to_txt] content quick view:\n >>', text_to_append[:char_preview].replace('\n', '\n >> '), '\n')
            file.close()
    except Exception as e:
        print(f'[append_text_to_txt] An error occurred while reading the file:\n {str(e)}')
        sys.exit()      


# This function is no longer in use.
def do_you_want_to_open_txt(message, path_txt):
    message = message + ' [Y/N]'
    string_ques = input(message)
    string_ques = string_ques.lower()
    if ('yes' in string_ques) or ('ye' in string_ques) or ('y' in string_ques) or ('ok' in string_ques) \
        or ('sure' in string_ques) or ('go' in string_ques):
        print('User agreed to proceed.', string_ques)
        try:
            # Attempt to open the text file
            with open(path_txt, 'r') as file:
                print(f"Contents of {path_txt}:\n")
                print(file.read())
            # Exit the program after displaying the file content
            sys.exit()
        except FileNotFoundError:
            print(f"The file at {path_txt} was not found.")
            sys.exit(1)
        except Exception as e:
            print(f"An error occurred: {e}")
            sys.exit(1)
    elif ('no' in string_ques) or ('n' in string_ques):
        print('User chose to stop.', string_ques)
        sys.exit()
    else:
        print('[Invalid Input] I will just keep moving on.\n', string_ques)




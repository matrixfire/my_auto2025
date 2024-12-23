import pyperclip

def clipboard_to_list():
    """
    Reads text from the clipboard, splits it into a list using new lines as separators,
    and returns the list.
    """
    # Get the text from the clipboard
    clipboard_text = pyperclip.paste()
    
    # Split the text into a list based on new lines
    text_list = clipboard_text.splitlines()
    
    # Return the list
    return text_list

# Example usage
if __name__ == "__main__":
    result = clipboard_to_list()
    print("List from clipboard text:")
    print(len(result))



def list_to_clipboard(lst):
    """
    Converts a list to a string with new lines as separators and copies it to the clipboard.
    """
    # Join the list elements with new lines
    text = "\n".join(lst)
    
    # Copy the text to the clipboard
    pyperclip.copy(text)
    print("List copied to clipboard.")





def check_existence(list_a, list_b):
    """
    For each item in list A, check if any item from list B exists in it.
    If a match is found, add the matched item to the result list.
    Otherwise, add "NO EXISTS".
    """
    result = []
    
    for item_a in list_a:
        found = False
        for item_b in list_b:
            if item_b in item_a:
                result.append(item_b)
                found = True
                break
        if not found:
            result.append("NO EXISTS")
    
    return result

# Example usage
list_a = ["山东黄金矿业股份有限公司", "北京大学", "中国科学技术大学"]
list_b = ["黄金", "北京", "清华"]

result = check_existence(list_a, list_b)
print("Result list:")
print(result)





















import pyperclip
from openai import OpenAI
import time

API_KEY = "Bearer sk-NpvUEGWHfd45VYyaOXwhWA40xZsHCrOg98SbdKleI4BJv320"
BASE_URL = "https://api.deepbricks.ai/v1/"
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)


all_text_lt = []



def generate_chat_completion(messages, model="GPT-4o-mini", max_tokens=2048, n=1, stop=None, temperature=0.8, stream=True):
    """
    Generate a chat completion using OpenAI's API.
    
    Args:
        messages (list): A list of messages for the chat.
        model (str): The model to use for the completion. Default is "GPT-3.5-turbo".
        max_tokens (int): The maximum number of tokens to generate in the response.
        n (int): Number of completions to generate for each prompt.
        stop (str or list): The stopping sequence(s) where the API will stop generating further tokens.
        temperature (float): Controls randomness in the output. Lower values make the output more deterministic.
        stream (bool): Whether to stream the response. Default is True.
    
    Returns:
        str: The assistant's response.
    """
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        n=n,
        stop=stop,
        temperature=temperature,
        stream=stream
    )
    
    # Collecting the complete response
    full_response = ""
    for chunk in completion:
        full_response += chunk.choices[0].delta.content if chunk.choices[0].delta.content else ""
    
    return full_response.strip()



def clipboard_chat(initial_prompt, max_history_length=5):
    """
    Start a chat session using clipboard input, keeping the initial prompt 
    and the most recent messages within a specified limit.
    
    Args:
        initial_prompt (str): The initial system message for context.
        max_history_length (int): The number of user/assistant messages to retain.
    """
    messages = [{"role": "system", "content": initial_prompt}]
    print("Chat session started with initial system message.")
    print(generate_chat_completion(messages))

    for k, v in enumerate(total):
        # input(f"Press Enter to get text from sublist({k})...")
        # time.sleep(1)
        clipboard_text = str(v) # pyperclip.paste()
        if clipboard_text:
            print(f"Using the data to promot chatgpt: '{clipboard_text}'\n")
            messages.append({"role": "user", "content": clipboard_text})

            # Adjust the message history to keep the system message, latest user input, 
            # and up to the max_history_length of previous user/assistant exchanges.
            if len(messages) > max_history_length + 2:  # +2 to account for system message and latest user input
                messages = [messages[0]] + messages[-(max_history_length + 1):]

            # Generate the assistant's response
            assistant_response = generate_chat_completion(messages)

            # Copy the response to clipboard
            pyperclip.copy(assistant_response)
            extracted_list = convert_to_list(assistant_response)
            print(len(extracted_list))
            all_text_lt.extend(extracted_list)

            print("Assistant:", assistant_response)
        else:
            print("Clipboard is empty. Please copy some text.")



def bot():
    input("Press Enter to get started...")
    initial_prompt = """
从现在开始，我给你提供一些中国的公司， 你帮我给出各个公司所在的省份，以及所属的行业，以python的格式给我即可
例如：
companies = [
    {"name": "中国电建集团山东电力建设第一工程有限公司", "province": "山东省", "industry": "电力工程"},
    {"name": "临沂天炬节能材料科技有限公司", "province": "山东省", "industry": "节能材料"},]
。从此刻起，我所有给你的提示，都只是公司名，你需要转化为companies = [
    {"name": "中国电建集团山东电力建设第一工程有限公司", "province": "山东省", "industry": "电力工程"},
    {"name": "临沂天炬节能材料科技有限公司", "province": "山东省", "industry": "节能材料"},]
这样的格式如果理解，说yes"""
    clipboard_chat(initial_prompt)


import ast

def convert_to_list(input_string):
    try:
        # Remove the 'companies = ' part and also any unwanted characters like "```python" and "```"
        cleaned_string = input_string.replace("```python", "").replace("```", "").strip()
        cleaned_string = cleaned_string.split('=', 1)[-1].strip()  # Remove 'companies = ' part
        
        # Convert the cleaned string to a list object using ast.literal_eval
        company_list = ast.literal_eval(cleaned_string)
        return company_list
    except Exception as e:
        print(f"Error: {e}")
        return []




if __name__ == "__main__":
    try:
        bot()
    except KeyboardInterrupt:
        print(all_text_lt)


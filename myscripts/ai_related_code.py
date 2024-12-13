API_KEY = "Bearer sk-NpvUEGWHfd45VYyaOXwhWA40xZsHCrOg98SbdKleI4BJv320"

import pyperclip
from openai import OpenAI
import time

API_KEY = "Bearer sk-NpvUEGWHfd45VYyaOXwhWA40xZsHCrOg98SbdKleI4BJv320"
BASE_URL = "https://api.deepbricks.ai/v1/"
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def generate_chat_completion(messages, model="GPT-4o-mini", max_tokens=1024, n=1, stop=None, temperature=0.8, stream=True):
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

def clipboard_chat_(initial_prompt):
    """
    Start a chat session using clipboard input.
    
    Args:
        initial_prompt (str): The initial prompt to set up the conversation.
    
    Returns:
        None
    """
    messages = [{"role": "system", "content": initial_prompt}]
    print("Chat session started. Press Enter to use clipboard text as input.")

    while True:
        input("Press Enter to get text from clipboard...")
        
        clipboard_text = pyperclip.paste()
        if clipboard_text:
            print(f"Using clipboard text: '{clipboard_text}'")
            messages.append({"role": "user", "content": clipboard_text})

            # Generate the assistant's response
            assistant_response = generate_chat_completion(messages)

            # Copy the response to clipboard
            pyperclip.copy(assistant_response)
            print("Assistant:", assistant_response)
            print("Response copied to clipboard!")
        else:
            print("Clipboard is empty. Please copy some text.")


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

    while True:
        input("Press Enter to get text from clipboard...")
        
        clipboard_text = pyperclip.paste()
        if clipboard_text:
            print(f"Using clipboard text: '{clipboard_text}'")
            messages.append({"role": "user", "content": clipboard_text})

            # Adjust the message history to keep the system message, latest user input, 
            # and up to the max_history_length of previous user/assistant exchanges.
            if len(messages) > max_history_length + 2:  # +2 to account for system message and latest user input
                messages = [messages[0]] + messages[-(max_history_length + 1):]

            # Generate the assistant's response
            assistant_response = generate_chat_completion(messages)

            # Copy the response to clipboard
            pyperclip.copy(assistant_response)
            print("Assistant:", assistant_response)
        else:
            print("Clipboard is empty. Please copy some text.")



def bot():
    input("Press Enter to set initalial prompt text from clipboard...")
    initial_prompt = pyperclip.paste() or "You are a helpful assistant."
    clipboard_chat(initial_prompt)



if __name__ == "__main__":
    bot()







###########################################


import os
import re
import shutil
import pyperclip

def move_file_and_generate_path():
    # Step 1: Get the file path from the clipboard
    file_path = pyperclip.paste().strip('"')

    # Check if the file path is valid
    if not os.path.isfile(file_path):
        print("The path provided is not valid.")
        return

    # Step 2: Define the target folder
    target_folder = r"F:\BaiduNetdiskDownload\已经上传Youtube视频"
    
    # Step 3: Move the file to the target folder
    try:
        shutil.move(file_path, os.path.join(target_folder, os.path.basename(file_path)))
        print(f"Moved file to {target_folder}")
    except Exception as e:
        print(f"Error moving file: {e}")
        return

    # Step 4: Extract the product ID from the filename
    filename = os.path.basename(file_path)
    match = re.search(r'(\d+)', filename)

    if match:
        product_id = match.group(1)
        # Step 5: Generate the new path
        new_path = rf"G:\x\t2\产品详情\{product_id}"
        
        # Step 6: Copy the new path to the clipboard
        pyperclip.copy(new_path)
        print(f"Generated path: {new_path} and copied to clipboard.")
    else:
        print("No product ID found in the filename.")




import os
import pyperclip as p
from PIL import Image
import pytesseract

def extract_text_from_image(image_path):
    # Open the image file
    img = Image.open(image_path)
    gray_img = img.convert('L')
    # Specify the path to the Tesseract executable
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    # Use pytesseract to extract text
    text = pytesseract.image_to_string(gray_img)
    return text

ocr = extract_text_from_image

def main(folder_path=''):
    if not folder_path:
        folder_path = p.paste()
    def remove_empty_lines(text):
        lines = text.split('\n')
        non_empty_lines = filter(lambda line: line.strip(), lines)
        return '\n'.join(non_empty_lines)

    all_text = ""
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                try:
                    all_text += (ocr(file_path) + '\n')
                    print(f"{file_path} extracted.")
                except PermissionError as e:
                    print(f"Permission error for file {file_path}: {e}")
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

    result = remove_empty_lines(all_text)
    p.copy(result)
    print(result)


move_file_and_generate_path()；main()

'''
SOME prompts:

We are a company in China with brand name Reobrix, which is a leading building block manufacturer based in China, specializing in high-quality, LEGO-like bricks. Our innovative building sets are designed to inspire creativity and provide a unique building experience for enthusiasts of all ages. With a diverse range of product collections, including Block Gun Collection, Submarine Series, Military Aircraft Collection, Cars Collection, Power Engineering Series, and many more, we cater to a wide array of interests and hobbies.

At Reobrix, we are dedicated to the construction and development of brand culture, creativity, and high standards of quality. Our products are sold in over 150 countries through various channels such as e-commerce, shopping malls, supermarkets, and specialty stores. We take pride in our detailed and realistic models, each crafted with precision and care, ensuring an engaging and rewarding assembly experience.

Our latest offerings include highly detailed models like the Reobrix Cathedral of Notre Dame, UCS-Style Star Shuttle, and the Scorpion Submachine Gun, among others. These models not only provide an immersive building experience but also serve as magnificent display pieces.

Our website url is https://reobrix.com/;  And my email is info@reobrix.com and bill@reobrix.com.

We have plans to collaborate with influencers by providing free samples for them to create and share videos and pictures, helping to showcase our products to a broader audience. Our commitment to quality and innovation has earned us a loyal customer base and long-term partnerships with well-known brands. And we are also looking for moc designers to contribute theirs works for us, and we can pay and buy from them.


Below I will keep providing words introduction for our models, I will write made youtube video and instagram posts for it,based on it, you should make me ：

1, youtube video description and its title
2, instagram post 

Be sure to include our brand name "Reobrix" to enhance seo, and adding our emails in it.

'''
import shelve
import pyperclip
import sys
import csv
import os
import lorem
import datetime
import json

# Constants
MARKDOWN_TEMPLATE = """
**<span style="color:red">Key:</span>**
{key}<br>
**<span style="color:green">Value:</span>**
{value}
---
"""

# Setup Directories and Shelve
def setup_directories():
    script_dir = os.path.dirname(__file__)
    data_dir = os.path.join(os.path.dirname(script_dir), 'mcb')
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

def setup_shelve(data_dir):
    shelve_filename = os.path.join(data_dir, 'mcb')
    return shelve.open(shelve_filename)

# Export and Import Functions
def export_to_csv(my_shelf, filename, data_dir):
    filepath = os.path.join(data_dir, filename)
    with open(filepath, 'w', newline='') as csvfile:
        fieldnames = ['key', 'value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for key in my_shelf.keys():
            writer.writerow({'key': key, 'value': my_shelf[key]})

def import_from_csv(my_shelf, filename, data_dir):
    filepath = os.path.join(data_dir, filename)
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            my_shelf[row['key']] = row['value']

# Clipboard Operations
def save_clipboard(my_shelf, keyword, message=None):
    value = pyperclip.paste()
    if message:
        value += f"\n***Bill Super Clipboard-{message}***"
    my_shelf[keyword] = value

def append_to_clipboard(my_shelf, keyword):
    new_value = pyperclip.paste()
    old_value = my_shelf.get(keyword, '')
    combined_value = f"{old_value}\n\n\n{new_value}"
    my_shelf[keyword] = combined_value

def delete_clipboard(my_shelf, keyword):
    if keyword and keyword in my_shelf:
        del my_shelf[keyword]
    else:
        print("Keyword for deletion not specified or does not exist.")

def list_clipboard(my_shelf, keys_only=False):
    if keys_only:
        formatted_keys = "\n".join(
            f"{key}: {my_shelf[key].split('***Bill Super Clipboard-')[-1].rstrip('***')}" if '***Bill Super Clipboard-' in my_shelf[key] else key
            for key in my_shelf.keys()
        )
        pyperclip.copy(formatted_keys)
        print(formatted_keys)
    else:
        formatted_list = "\n".join(MARKDOWN_TEMPLATE.format(key=key, value=my_shelf[key]) for key in my_shelf.keys())
        pyperclip.copy(formatted_list)
        print(formatted_list)

def clear_shelve(my_shelf):
    my_shelf.clear()
    print("All data cleared from the shelve.")

def retrieve_clipboard(my_shelf, keyword):
    if keyword in my_shelf:
        content = my_shelf[keyword]
        if '{{' in content and '}}' in content:
            content_to_paste = pyperclip.paste()
            content = content.replace(content[content.find('{{'):content.find('}}')+len('}}')], content_to_paste)
        if "***Bill Super Clipboard-" in content:
            content = content.split("\n***Bill Super Clipboard-")[0]
        pyperclip.copy(content.strip().strip("\""))

def generate_lorem(option):
    if option == 1:
        pyperclip.copy(lorem.sentence().title())
    elif option == 2:
        pyperclip.copy(lorem.paragraph())

def generate_lorem_custom(word_count=None):
    if word_count is None:
        content = lorem.paragraph()
    else:
        words = []
        while len(words) < word_count:
            words.extend(lorem.sentence().split())
        content = ' '.join(words[:word_count])
    if len(content.split()) > 20:
        content = content.rstrip('.') + "."
    pyperclip.copy(content)
    print(f"Generated lorem ipsum text ({len(content.split())} words) copied to clipboard.")

def generate_git_commands(message=None):
    if not message:
        message = datetime.datetime.now().strftime("%B %d, %Y, %I:%M %p")
    git_commands = f'git add .\ngit commit -m "{message}"\ngit push'
    pyperclip.copy(git_commands)
    print(git_commands)

def convert_to_json(my_shelf):
    data_dict = {key: my_shelf[key] for key in my_shelf.keys()}
    json_string = json.dumps(data_dict, indent=4)
    pyperclip.copy(json_string)
    print("JSON string copied to clipboard")

def display_help():
    help_text = """
    Multi-Clipboard Script Usage:
    -----------------------------
    -save <keyword> [-m "message"] : Save the current clipboard content under the specified keyword.
                                    Optionally, add a brief usage message.
    -save+ <keyword>               : Append the current clipboard content to the specified keyword's content
                                    with three empty lines in between.
    -delete <keyword>              : Delete the content associated with the specified keyword.
    -delete                        : Prompt for keyword if not specified.
    -list                          : List all saved key-value pairs and copy them to the clipboard.
    -list -k                       : List all saved keys one per line and copy them to the clipboard.
    -export <filename.csv>         : Export all saved data to the specified CSV file (default: mydata.csv).
    -import <filename.csv>         : Import data from the specified CSV file (default: mydata.csv).
    -flush                         : Clear all data from the shelve database.
    -json                          : Convert all key-value pairs to a formatted JSON string and copy to clipboard.
    <keyword>                      : Retrieve the content associated with the specified keyword and copy it to the clipboard.
    -lorem1                        : Copy a lorem ipsum sentence to the clipboard.
    -lorem2                        : Copy a lorem ipsum paragraph to the clipboard.
    -git ["message"]               : Generate and copy Git commands to the clipboard.
                                     If no message is provided, use the current date as the commit message.
    -help                          : Display this help information and copy it to the clipboard.
    """
    print(help_text)
    pyperclip.copy(help_text)

# Command-line Interface
def main():
    data_dir = setup_directories()
    my_shelf = setup_shelve(data_dir)

    arg_len = len(sys.argv)
    if arg_len >= 2:
        action = sys.argv[1].lower()
        if action == '-save' and arg_len >= 3:
            keyword = sys.argv[2]
            message = sys.argv[4] if arg_len >= 5 and sys.argv[3] == '-m' else None
            save_clipboard(my_shelf, keyword, message)
        elif action == '-save+' and arg_len >= 3:
            keyword = sys.argv[2]
            append_to_clipboard(my_shelf, keyword)
        elif action == '-delete':
            keyword = sys.argv[2] if arg_len == 3 else None
            delete_clipboard(my_shelf, keyword)
        elif action == '-list':
            keys_only = arg_len == 3 and sys.argv[2] == '-k'
            list_clipboard(my_shelf, keys_only)
        elif action == '-export':
            filename = sys.argv[2] if arg_len == 3 else 'mydata.csv'
            export_to_csv(my_shelf, filename, data_dir)
        elif action == '-import':
            filename = sys.argv[2] if arg_len == 3 else 'mydata.csv'
            import_from_csv(my_shelf, filename, data_dir)
        elif action == '-flush':
            clear_shelve(my_shelf)
        elif action == '-help':
            display_help()
        elif action == '-lorem1':
            generate_lorem(1)
        elif action == '-lorem2':
            generate_lorem(2)
        elif action == '-lm' and arg_len >= 3:
            num = int(sys.argv[2])
            generate_lorem_custom(num)            
        elif action == '-git':
            message = sys.argv[2].strip('"') if arg_len == 3 else None
            generate_git_commands(message)
        elif action == '-json':
            convert_to_json(my_shelf)
        else:
            retrieve_clipboard(my_shelf, action)

    my_shelf.close()

if __name__ == "__main__":
    main()

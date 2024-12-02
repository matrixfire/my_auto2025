'''
Django folders set up automatically
'''

import os

def setup_django_app(app_path):
    # Extract app name from the path
    app_name = os.path.basename(app_path)

    # Define paths for urls.py, forms.py, templates, and static directories
    urls_path = os.path.join(app_path, 'urls.py')
    forms_path = os.path.join(app_path, 'forms.py')
    templates_path = os.path.join(app_path, 'templates', app_name)
    static_path = os.path.join(app_path, 'static', app_name)
    templatetags_path = os.path.join(app_path, 'templatetags')
    app_tags_path = os.path.join(templatetags_path, f'{app_name}_tags.py')

    # Create urls.py if it does not exist
    if not os.path.exists(urls_path):
        with open(urls_path, 'w') as urls_file:
            urls_file.write(f"""
from django.urls import path
from . import views

app_name = '{app_name}'

urlpatterns = [
    path('', views.index, name='index'),
    # Add other paths here
]
""")
 
    # Create forms.py if it does not exist (empty file)
    if not os.path.exists(forms_path):
        open(forms_path, 'a').close()

    # Create templates and static directories if they don't exist
    for directory in (templates_path, static_path):
        os.makedirs(directory, exist_ok=True)

    # Create templatetags directory if it doesn't exist
    if not os.path.exists(templatetags_path):
        os.makedirs(templatetags_path, exist_ok=True)
        
        # Add __init__.py to make it a Python package
        init_path = os.path.join(templatetags_path, '__init__.py')
        open(init_path, 'a').close()
        
        # Create app_tags.py for custom template tags
        open(app_tags_path, 'a').close()

# Assign setup_django_app to a variable (potentially for later use)
dj = setup_django_app













#  THIS ONE IS GOOD!!!!
import pyperclip
import re

def extract_image_references_from_clipboard():
    '''Django helper: From clipboard html code extract all src attribute'''
    # Get HTML content from the clipboard
    html_content = pyperclip.paste()

    # Define a regex pattern to match image URLs in any attribute
    pattern = r'[\w-]+="([^"]+\.(?:jpg|jpeg|png|gif|ico|svg|bmp))"'

    # Find all matches for the pattern
    matches = re.findall(pattern, html_content, re.IGNORECASE)

    # Print the extracted image references
    print("Extracted image references:")
    for img in matches:
        print(img)



def modify_image_references_from_clipboard(modify_func):
    '''Django helper: modify all img src attribute, with some function to static format'''
    # Get HTML content from the clipboard
    html_content = pyperclip.paste()

    # Define a regex pattern to match image URLs in any attribute
    pattern = r'''(href|src|data-[\w-]+)=["']([^"]+\.(?:jpg|jpeg|png|gif|ico|svg|bmp))["']'''

    # Define the replacement function to be used with re.sub
    def replacement(match):
        attribute = match.group(1)
        img_reference = match.group(2)
        new_reference = modify_func(img_reference)
        return f'{attribute}="{new_reference}"'

    # Use re.sub to replace the pattern with the modified references
    modified_html_content = re.sub(pattern, replacement, html_content, flags=re.IGNORECASE)

    # Print or copy the modified content back to the clipboard
    pyperclip.copy(modified_html_content)
    print(modified_html_content)


 
def prefix_static(prefix):
    ''' usage: modify_image_references_from_clipboard(prefix_static("fuck/"))'''
    def modify(img_reference):
        new_reference = prefix + img_reference
        result = f"{{% static \'{new_reference}\' %}}"
        return result
    return modify    

modify_image_references_from_clipboard(prefix_static("shop/")



template_names = [
    'about-us.html',
    'blog-single-post.html',
    'blog.html',
    'checkout.html',
    'contacts.html',
    'index.html',
    'privacy.html',
    'search-results.html',
    'shop.html',
    'single-product.html'
]

import pyperclip as p



def generate_view_functions(template_names):
    view_functions = []

    for template in template_names:
        view_name = template.replace('.html', '').replace('-', '_')
        function_definition = f"""
def {view_name}(request):
    return render(request, 'core/{template}')
"""
        view_functions.append(function_definition)

    # Join all function definitions into a single string
    views_code = "\n".join(view_functions)
    p.copy(views_code)

def generate_url_patterns(template_names):
    url_patterns = []

    for template in template_names:
        view_name = template.replace('.html', '').replace('-', '_')
        url_pattern = template.replace('.html', '').replace('_', '-')
        url_pattern_line = f"path('{url_pattern}/', views.{view_name}, name='{view_name}'),"
        url_patterns.append(url_pattern_line)

    # Join all URL patterns into a single string
    urls_code = "\n".join(url_patterns)
    p.copy(urls_code)


























# modify_image_references_from_clipboard(prefix_static("fuck/"))



def modify_customized_references_from_clipboard(modify_func):
    # Get HTML content from the clipboard
    html_content = pyperclip.paste()

    # Define a regex pattern to match image URLs in any attribute
    pattern = r'(href|action)="([^"]+\.(?:html))"'

    # Define the replacement function to be used with re.sub
    def replacement(match):
        attribute = match.group(1)
        img_reference = match.group(2)
        new_reference = modify_func(img_reference.replace(".html","").replace("-","_"))
        return f'{attribute}="{{% url \'{new_reference}\' %}}"'

    # Use re.sub to replace the pattern with the modified references
    modified_html_content = re.sub(pattern, replacement, html_content, flags=re.IGNORECASE)

    # Print or copy the modified content back to the clipboard
    pyperclip.copy(modified_html_content)
    print(modified_html_content)


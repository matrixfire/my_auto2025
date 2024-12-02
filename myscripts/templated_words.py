"""
This script generates a list of formatted strings based on a template and several lists of values.

1. **Template Definition**: A template string with placeholders is defined. These placeholders will be replaced by values from the provided lists.
2. **List Definitions**: Several lists of strings are defined, each containing potential values for different parts of the final formatted strings.
3. **Combination Generation**: The script uses the `itertools.product` function to generate all possible combinations of values from the provided lists.
4. **String Formatting**: Each combination of values is used to replace placeholders in the template, producing a formatted string for each combination.
5. **Saving Results**: The resulting list of formatted strings is saved to a JSON file named `words1.json`.
6. **Output**: The script prints the number of generated formatted strings.

The purpose of this script is to create a variety of personalized or templated messages based on predefined patterns and options.
"""

import pyperclip as p  # Importing the pyperclip module for clipboard operations (though it's not used in this script)

import itertools  # Importing itertools for generating Cartesian products
import json  # Importing json for JSON file handling

from pathlib import Path  # Importing Path for file path operations

def generate_product(template, *lists):
    """
    Generate formatted strings based on a template and multiple lists of values.

    Args:
        template (str): A string with placeholders in the format {{0}}, {{1}}, etc.
        *lists (list of list of str): Lists of strings to be used for generating combinations.

    Returns:
        list of str: A list of formatted strings where each placeholder in the template is replaced 
                     by a corresponding value from the lists.
    """
    results = []
    # Generate all combinations of elements from the provided lists
    for combination in itertools.product(*lists):
        # Create a formatted string by replacing placeholders in the template
        formatted_string = template
        for i, value in enumerate(combination, 0):  # Replace placeholders with values
            formatted_string = formatted_string.replace(f"{{{{{i}}}}}", value)
        results.append(formatted_string)
    return results


# Define the template with placeholders
template2 = '''
{{0}},

{{1}} {{2}}

1. {{3}}

2. {{4}}

3. {{5}}

{{6}}

Best Regards,

'''
template2 = template2.strip()  # Remove leading and trailing whitespace from the template

# Define lists of possible values for each placeholder
tp0 = ["Hi there", "Hello there", "Hi", "Hello"]
tp1 = ["Hope you're doing great!", "I hope this email finds you well."]
tp2 = ["I’m Bill from Reobrix, where creativity meets quality in building block design. We're reaching out to explore opportunities for collaboration in several exciting areas:", "We're all about sparking creativity with our building blocks at Reobrix. There's something for everyone, whether you're looking for a new project or a gift. Check out our latest at Reobrix.com and start building!"]
tp3 = ["For Customers & Distributors: Explore our innovative building blocks and consider joining our global network. Check out our products at https://reobrix.com/.", "For Our Customers: Discover special collections and start your creative journey. It's all fun and inspiration."]
tp4 = ["For Influencers: Love building and sharing? Let's work together and spread the joy of building. Exciting rewards await!", "For Influencers: Help us inspire builders by showcasing our models. We offer exclusive access to our latest products for your creative showcases."]
tp5 = ["For MOC Fans: Got cool designs? We'd love to see and possibly collaborate. Show us what you've got!", "For MOC Fans: We’re eager to discover and purchase unique building block designs to turn them into commercial models that inspire globally."]
tp6 = ["If you’re interested in buying, promoting, or partnering with us, please reply to this email. Let’s create something amazing together!", "Interested in any of these? Just hit us up at Reobrix. Can't wait to build something amazing together."]

# Collect the lists into a single list
lists = [tp0, tp1, tp2, tp3, tp4, tp5, tp6]

# Generate formatted strings based on the template and lists
resulting_strings = generate_product(template2, *lists)

# Write the resulting strings to a JSON file
path = Path('words1.json')
words = json.dumps(resulting_strings)
path.write_text(words)

# Print the number of generated strings
print(len(resulting_strings))

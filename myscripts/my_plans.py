import random
from collections import Counter
import pyperclip

def parse_plans(file_path):
    plans = []
    forced_plans = []
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                parts = line.split(' ')
                plan_name = parts[0]
                weight_or_times = parts[1]
                
                # Handle the special '*' case
                if weight_or_times.startswith('*'):
                    times = int(weight_or_times[1:])
                    forced_plans.append((plan_name, times))
                else:
                    weight = int(weight_or_times)
                    plans.append((plan_name, weight))
    
    return plans, forced_plans

def generate_todo_list(plans, forced_plans, total_count):
    todo_list = []

    # Add forced plans first
    for plan, times in forced_plans:
        todo_list.extend([plan] * times)

    # Calculate the total weight and prepare the weighted plans
    weighted_plans = []
    for plan, weight in plans:
        weighted_plans.extend([plan] * weight)
    
    # Randomly select from weighted plans until we fill the rest of the list
    remaining_count = total_count - len(todo_list)
    todo_list.extend(random.choices(weighted_plans, k=remaining_count))
    
    return todo_list

def base6_index(i):
    """ Convert a decimal index to a base-6 representation with 3 digits (e.g., 111 to 666) """
    return f"{i//36 + 1}{(i//6) % 6 + 1}{i % 6 + 1}"

def print_todo_list(todo_list, total_count):
    # Print the random to-do list with base-6 index
    output = []
    for i, task in enumerate(todo_list, start=1):
        base6_idx = base6_index(i-1)  # Convert 0-based index to base-6
        output.append(f"{base6_idx}. {task}")
    
    # Join the list into a string
    output_str = "\n".join(output)
    print(output_str)
    
    # Count occurrences of each plan
    task_counts = Counter(todo_list)

    # Print the proportion and the number of times each plan appeared
    output_str += "\n\nProportions:\n"
    for plan, count in sorted(task_counts.items(), key=lambda x: x[1], reverse=True):
        proportion = (count / total_count) * 100
        output_str += f"{plan}: appeared {count} times ({proportion:.2f}%)\n"
    
    # Copy the list to clipboard
    pyperclip.copy(output_str)
    print("\nThe list has been copied to the clipboard.")

def main(file_path, total_count=216):
    plans, forced_plans = parse_plans(file_path)
    todo_list = generate_todo_list(plans, forced_plans, total_count)
    
    # Randomize the final todo list
    random.shuffle(todo_list)
    
    # Print the todo list, proportions and copy to clipboard
    print_todo_list(todo_list, total_count)

# Example usage
file_path = 'plans.txt'  # Your file path here
todo_list = main(file_path)

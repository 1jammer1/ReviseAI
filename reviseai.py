import argparse
import ollama
import os
import ast

def generate_code(prompt):
    """Generate code using the Ollama API."""
    response = ollama.chat(prompt)
    return response['content']

def index_files(directory):
    """Index Python files and return a dictionary of file names and their content."""
    file_index = {}
    for filename in os.listdir(directory):
        if filename.endswith('.py'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                file_index[filename] = file.read()
    return file_index

def analyze_file_content(content):
    """Analyze the content of a file to understand its purpose (simple heuristics)."""
    try:
        tree = ast.parse(content)
        return [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    except SyntaxError:
        return []

def choose_files_to_fix(file_index, prompt):
    """Choose relevant files based on user prompt."""
    relevant_files = []
    for filename, content in file_index.items():
        # Analyze content for functions and check if prompt relates to any function
        functions = analyze_file_content(content)
        if any(fn in prompt for fn in functions):
            relevant_files.append(filename)
    return relevant_files

def process_file(file_path, action, prompt):
    """Process a single file: read, generate/fix code, and save the result."""
    with open(file_path, 'r') as file:
        code = file.read()

    if action == 'fix':
        prompt = f"Fix the following Python code:\n\n{code}"
    else:
        prompt = f"Create Python code for:\n\n{prompt}"

    print(f"Processing {file_path}...")
    generated_code = generate_code(prompt)

    # Save the modified code back to a new file
    output_file_name = os.path.splitext(file_path)[0] + '_fixed.py' if action == 'fix' else os.path.join(os.getcwd(), f"{prompt.replace(' ', '_').lower()}.py")
    
    with open(output_file_name, 'w') as output_file:
        output_file.write(generated_code)
    
    print(f"Saved to {output_file_name}")

def process_directory(directory, action, prompt):
    """Process files in the directory based on the action and prompt."""
    file_index = index_files(directory)
    files_to_process = choose_files_to_fix(file_index, prompt) if action == 'fix' else file_index.keys()

    for filename in files_to_process:
        file_path = os.path.join(directory, filename)
        process_file(file_path, action, prompt)

def main():
    parser = argparse.ArgumentParser(description='AI Code Creator/Fixer using Ollama')
    parser.add_argument('action', choices=['create', 'fix'], help='Action to perform: create or fix code')
    parser.add_argument('prompt', help='Prompt for the AI to generate/fix code')

    args = parser.parse_args()

    current_directory = os.getcwd()

    process_directory(current_directory, args.action, args.prompt)

if __name__ == "__main__":
    main()

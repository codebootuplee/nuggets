import os
import re
from cookiecutter.main import cookiecutter

# Helper function to convert a string to kebab-case (dash-separated)
def to_kebab_case(name):
    return re.sub(r'(?<!^)(?=[A-Z])', '-', name).lower()

# Helper function to convert a string to camelCase
def to_camel_case(name):
    name_parts = name.split('-')
    return name_parts[0] + ''.join(part.capitalize() for part in name_parts[1:])

# Function to create a new project directory from a template using Cookiecutter
def create_projects_from_template(template_dir, root_dir):
    if not os.path.exists(template_dir):
        raise FileNotFoundError(f"Template directory '{template_dir}' not found.")

    project_dirs = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]

    for project_name in project_dirs:
        kebab_case_name = to_kebab_case(project_name)
        camel_case_name = to_camel_case(kebab_case_name)
        project_path = os.path.join(root_dir, project_name)
        new_project_dir = os.path.join(project_path, f"{kebab_case_name}-chart")

        # Run Cookiecutter with the project-specific context
        cookiecutter(
            template_dir,
            no_input=True,
            extra_context={
                'kebab_case_name': kebab_case_name,
                'camelCaseName': camel_case_name
            },
            output_dir=project_path
        )

        print(f"Project '{project_name}' created successfully with kebab-case='{kebab_case_name}' and camelCase='{camel_case_name}'.")

# Example usage
if __name__ == "__main__":
    template_directory = input("Enter the path to the template directory: ")
    root_directory = input("Enter the path to the root directory with project folders: ")

    try:
        create_projects_from_template(template_directory, root_directory)
    except Exception as e:
        print(f"Error: {e}")

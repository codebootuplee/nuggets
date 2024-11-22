import os
import subprocess
import argparse

def is_gradle_project(path):
    """Check if the given directory is a Gradle project."""
    return any(
        os.path.isfile(os.path.join(path, gradle_file))
        for gradle_file in ["build.gradle", "build.gradle.kts"]
    )

def run_gradle_task(project_path, task):
    """
    Run a Gradle task in the given project directory.
    Returns True if the task succeeds, False otherwise.
    """
    try:
        # Change to the project directory
        original_dir = os.getcwd()
        os.chdir(project_path)

        # Execute the Gradle task
        subprocess.run(["./gradlew", task], check=True)
        print(f"Task '{task}' succeeded in project: {project_path}")
        return True
    except subprocess.CalledProcessError:
        print(f"Task '{task}' failed in project: {project_path}")
        return False
    except FileNotFoundError:
        print(f"No Gradle wrapper found in project: {project_path}")
        return False
    finally:
        # Change back to the original directory
        os.chdir(original_dir)

def find_gradle_projects_and_run_task(directory, task):
    """
    Traverse the directory tree starting at `directory`, find Gradle projects,
    and run the specified Gradle task in each project.
    Logs and returns a list of projects where the task failed.
    """
    failed_projects = []

    for root, dirs, _ in os.walk(directory):
        if is_gradle_project(root):
            success = run_gradle_task(root, task)
            if not success:
                failed_projects.append(root)
            # Skip traversing subdirectories of the Gradle project
            dirs[:] = []

    return failed_projects

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find Gradle projects and run a task.")
    parser.add_argument("directory", help="The root directory to start the search.")
    parser.add_argument("task", help="The Gradle task to run (e.g., build, test).")
    args = parser.parse_args()

    failed_projects = find_gradle_projects_and_run_task(args.directory, args.task)

    if failed_projects:
        print("\nThe following projects failed:")
        for project in failed_projects:
            print(f"- {project}")
    else:
        print("\nAll projects succeeded.")

import gitlab

# Initialize GitLab connection
gl = gitlab.Gitlab("https://gitlab.com", private_token="YOUR_ACCESS_TOKEN")

def create_epics_with_parent(group_id, titles, parent_epic_id):
    """
    Creates an epic for each title in the titles array and associates each with a parent epic.

    Parameters:
    - group_id (int): The ID of the GitLab group where the epics will be created.
    - titles (list of str): Array of titles for each new epic.
    - parent_epic_id (int): The ID of the parent epic to associate each new epic with.
    """
    try:
        group = gl.groups.get(group_id)
    except gitlab.exceptions.GitlabGetError:
        print(f"Could not access group with ID {group_id}.")
        return

    for title in titles:
        epic_data = {
            'title': title,
            'parent_id': parent_epic_id
        }

        # Create the epic in the specified group
        new_epic = group.epics.create(epic_data)
        print(f"Created epic '{title}' with ID {new_epic.id}, associated with parent epic ID {parent_epic_id}")

# Define the group ID, titles, and parent epic ID
group_id = 123  # Replace with the actual group ID
titles = ["Epic Title 1", "Epic Title 2", "Epic Title 3"]  # Replace with your epic titles
parent_epic_id = 456  # Replace with the actual parent epic ID

# Create epics with the specified parent
create_epics_with_parent(group_id, titles, parent_epic_id)

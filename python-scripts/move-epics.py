import gitlab

# Initialize GitLab connection
gl = gitlab.Gitlab("https://gitlab.com", private_token="YOUR_ACCESS_TOKEN")

def move_child_epics(old_parent_epic_global_id, new_parent_epic_global_id):
    """
    Move all child epics from one parent epic to another using global IDs.
    
    Parameters:
    - old_parent_epic_global_id (int): The global ID of the original parent epic.
    - new_parent_epic_global_id (int): The global ID of the new parent epic.
    """
    # Fetch the original parent epic using its global ID
    try:
        parent_epic = gl.epics.get(old_parent_epic_global_id)
        new_parent_epic = gl.epics.get(new_parent_epic_global_id)
    except gitlab.exceptions.GitlabGetError:
        print(f"Epic with ID {old_parent_epic_global_id} or {new_parent_epic_global_id} not found.")
        return

    # Get child epics and move each to the new parent epic
    for child_epic in parent_epic.children.list():
        print(f"Moving epic {child_epic.id} from parent {old_parent_epic_global_id} to new parent {new_parent_epic_global_id}")
        child_epic.parent_id = new_parent_epic_global_id
        child_epic.save()
        print(f"Epic {child_epic.id} moved successfully.")

# Define the global epic IDs
old_parent_epic_global_id = 123  # Replace with the original parent epic's global ID
new_parent_epic_global_id = 456  # Replace with the new parent epic's global ID

# Move the child epics
move_child_epics(old_parent_epic_global_id, new_parent_epic_global_id)

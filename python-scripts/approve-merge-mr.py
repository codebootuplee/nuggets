import gitlab
import argparse

def find_merge_requests_with_message(gl, root_group_id, commit_message):
    """
    Find all merge requests in the given root group's hierarchy that have the specified commit message.
    """
    matching_mrs = []

    # Fetch all subgroups and projects within the root group
    root_group = gl.groups.get(root_group_id)
    projects = root_group.projects.list(all=True, include_subgroups=True)

    for project in projects:
        try:
            # Get detailed project object
            project_obj = gl.projects.get(project.id)

            # List all merge requests for the project
            merge_requests = project_obj.mergerequests.list(state="opened", all=True)

            for mr in merge_requests:
                # Fetch the MR's commits
                commits = mr.commits()
                for commit in commits:
                    if commit.message.strip() == commit_message.strip():
                        matching_mrs.append((project_obj, mr))
                        break  # Stop checking commits for this MR
        except Exception as e:
            print(f"Error fetching merge requests for project {project.path_with_namespace}: {e}")

    return matching_mrs

def approve_and_merge_mrs(matching_mrs):
    """
    Approve and merge the list of matching merge requests.
    """
    for project, mr in matching_mrs:
        try:
            # Approve the MR
            mr.approve()
            print(f"Approved MR #{mr.iid} in project {project.path_with_namespace}")

            # Merge the MR
            mr.merge(merge_commit_message="Merged by script")
            print(f"Merged MR #{mr.iid} in project {project.path_with_namespace}")
        except Exception as e:
            print(f"Error approving or merging MR #{mr.iid} in project {project.path_with_namespace}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find and process GitLab merge requests with a specific commit message."
    )
    parser.add_argument("gitlab_url", help="The GitLab instance URL (e.g., https://gitlab.com).")
    parser.add_argument("token", help="Your GitLab personal access token.")
    parser.add_argument("root_group_id", type=int, help="The ID of the root group to search.")
    parser.add_argument("commit_message", help="The commit message to search for.")
    args = parser.parse_args()

    # Authenticate with GitLab
    gl = gitlab.Gitlab(args.gitlab_url, private_token=args.token)

    # Find merge requests
    print("Searching for merge requests...")
    matching_mrs = find_merge_requests_with_message(gl, args.root_group_id, args.commit_message)

    if not matching_mrs:
        print("No merge requests found with the specified commit message.")
    else:
        print(f"Found {len(matching_mrs)} merge request(s) with the specified commit message.")
        approve_and_merge_mrs(matching_mrs)

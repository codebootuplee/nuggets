import gitlab

# Initialize a connection to GitLab (provide your GitLab URL and access token)
gl = gitlab.Gitlab('https://gitlab.example.com', private_token='YOUR_PERSONAL_ACCESS_TOKEN')

# Create a new project
project = gl.projects.create({
    'name': 'MyNewProject',
    'visibility': 'private'  # Set project visibility to private
})

# Create a branch protection rule for the 'main' branch (no direct push)
project.protectedbranches.create({
    'name': 'main',
    'push_access_level': gitlab.PROTECTED_BRANCH_NO_ONE,  # No direct push allowed
    'merge_access_level': gitlab.PROTECTED_BRANCH_MAINTAINER,  # Maintainer level merge access
})

# Enable the requirement for at least one approver on merge requests
approval_settings = project.approvals.update({
    'approvals_before_merge': 1  # Require at least 1 approver
})

# Create a personal access token for pipelines
token_data = project.access_tokens.create({
    'name': 'pipeline-token',
    'scopes': ['api'],
    'expires_at': None  # No expiration date, set this if you want to limit token lifespan
})

# Get the token string (for use in your pipelines)
pipeline_token = token_data.token

# Output the created pipeline token (you should store this securely)
print(f"Pipeline Token: {pipeline_token}")

print(f"Project '{project.name}' created successfully with push restrictions and MR approver rules.")

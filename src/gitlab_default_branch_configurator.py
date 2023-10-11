import requests
import urllib3

# GitLab API URL
api_url = ''

# Personal Access Token for authentication
personal_access_token = ""

# Disable SSL warnings (use with caution)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Headers for API requests containing the Personal Access Token
headers = {
    'PRIVATE-TOKEN': personal_access_token,
}

# Parameters for configuring the 'main' branch
parameters_main = {
    "name": "main",
    "push_access_level": 30,
    "merge_access_level": 30,
    "unprotect_access_level": 40,
    "allow_force_push": "false"
}

# Parameters for configuring the 'master' branch
parameters_master = {
    "name": "master",
    "push_access_level": 30,
    "merge_access_level": 30,
    "unprotect_access_level": 40,
    "allow_force_push": "false"
}

# Initialize page number for paginated requests
page = 1

# Dictionary to store project information (ID to name mapping)
project_info = {}

# Retrieve and store project information
while True:
    # Construct the URL for listing projects with pagination
    projects_url = f"{api_url}/projects?page={page}&per_page=100"  # Adjust per_page as needed

    # Send a GET request to fetch projects
    response = requests.get(projects_url, headers=headers, verify=False)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        projects = response.json()

        # If there are no more projects, break out of the loop
        if len(projects) == 0:
            break

        # Extract project IDs and names and add them to the dictionary
        for project in projects:
            project_id = project["id"]
            project_name = project["name"]
            project_info[project_id] = project_name

        # Increment the page number for the next request
        page += 1
    else:
        print(f"Failed to retrieve projects. Status code: {response.status_code}")
        break

# Iterate through projects and their branches
for project_id, project_name in project_info.items():
    print(f"Project ID: {project_id}, Project Name: {project_name}")

    try:
        # Construct the URL for listing branches, including stale branches
        branches_url = f'{api_url}/projects/{project_id}/repository/branches?per_page=100&all=true'

        # Send a GET request to fetch branches
        response = requests.get(branches_url, headers=headers, verify=False)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            branches = response.json()

            # Extract and print branch names
            branch_names = [branch['name'] for branch in branches]

            # Check if 'main' or 'master' exists among branches
            default_branch = None
            if 'main' in branch_names:
                default_branch = 'main'
            elif 'master' in branch_names:
                default_branch = 'master'

            # Handle the default branch based on its name
            if default_branch:
                print(f"Default branch found: {default_branch}")

                if default_branch == 'main':
                    # Configure the 'main' branch with specified parameters
                    response = requests.post(
                        f'{api_url}/projects/{project_id}/protected_branches',
                        headers=headers, verify=False, json=parameters_main)

                    # Handle a conflict (HTTP status code 409) if the branch already exists
                    if response.status_code == 409:
                        # Delete the existing 'main' branch protection
                        response_2 = requests.delete(
                            f'{api_url}/projects/{project_id}/protected_branches/main',
                            headers=headers, verify=False)

                        # Retry configuring the 'main' branch
                        response = requests.post(
                            f'{api_url}/projects/{project_id}/protected_branches',
                            headers=headers, verify=False, json=parameters_main)

                    print(response.json())

                elif default_branch == 'master':
                    # Configure the 'master' branch with specified parameters
                    response = requests.post(
                        f'{api_url}/projects/{project_id}/protected_branches',
                        headers=headers, verify=False, json=parameters_master)

                    # Handle a conflict (HTTP status code 409) if the branch already exists
                    if response.status_code == 409:
                        # Delete the existing 'master' branch protection
                        response_2 = requests.delete(
                            f'{api_url}/projects/{project_id}/protected_branches/master',
                            headers=headers, verify=False)

                        # Retry configuring the 'master' branch
                        response = requests.post(
                            f'{api_url}/projects/{project_id}/protected_branches',
                            headers=headers, verify=False, json=parameters_master)

                    print(response.json())
            else:
                print("Neither 'main' nor 'master' branch found.")
        else:
            print(f"Error: Unable to fetch branches. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {str(e)}")

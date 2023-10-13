# Gitlab Default Branch Configurator


This script is designed to automate the configuration of default branches, specifically 'main' and 'master', in GitLab projects. It utilizes the GitLab API to achieve this and is intended to be run in a secure environment with proper authentication.
Prerequisites

## Before using this script, ensure that you have the following prerequisites:

- GitLab API URL: You need to specify the GitLab API URL in the api_url variable.

- Personal Access Token: Obtain a Personal Access Token from GitLab and set it as the personal_access_token variable for authentication.

    Note: Keep your Personal Access Token confidential and secure.

- Python Libraries: You need to have the following Python libraries installed:
    - requests: You can install it using pip install requests.
    - urllib3: You can install it using pip install urllib3.


## Script Configuration

The script is configured with two sets of parameters:

- parameters_main: These parameters are used to configure the 'main' branch.
- parameters_master: These parameters are used to configure the 'master' branch.

You can adjust these parameters as needed to match your GitLab project's requirements. For example, you can modify the access levels or allow force pushing as necessary.
Usage

Provide the GitLab API URL and Personal Access Token in the script.

Run the script in your Python environment. It will perform the following actions:
- Retrieve a list of projects using pagination.
- Check for the existence of 'main' or 'master' branches in each project.
- If a default branch ('main' or 'master') is found, it configures the branch with the specified parameters.
- If a branch already exists with the same name, it will handle conflicts by deleting the existing protection and retrying the configuration.

## Caution

Be cautious while running this script in a production environment as it can modify project configurations.
Ensure that your Personal Access Token has the necessary permissions to perform these actions.

## Disclaimer

Use this script at your own risk. It is your responsibility to verify its functionality and ensure it aligns with your GitLab policies and procedures.

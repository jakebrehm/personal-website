"""
Module for generating projects to be displayed on the website.
"""

import json
import os
from pathlib import Path

import dotenv
import github
from github import AuthenticatedUser, GithubException

PROJECTS_FILENAME: str = "projects.json"


def read_blueprint(filepath: str | Path, encoding: str = "utf-8") -> list:
    """Reads the specified JSON file, returns data as a list of dictionaries."""
    with open(filepath, "r", encoding=encoding) as f:
        return json.load(f)


def update_description_from_github(
    project: dict,
    user: AuthenticatedUser,
) -> dict:
    """Updates the description of the specified project.

    If the project description is requested to be updated, the description
    is pulled from the live GitHub repository.
    """

    # Get the name of the GitHub repository if there is one
    try:
        github_repository = project["links"]["github"]
    except KeyError:
        # Pass the data through if there is no repository
        return project

    # Update the description from the live repository if requested
    if project.get("update_description", True):
        try:
            repository = user.get_repo(github_repository)
            description = repository.description
        except GithubException:
            description = None
        project["description"] = description
    return project


def clean_projects(projects: list, user: AuthenticatedUser) -> list:
    """Cleans the specified projects list."""
    for p, project in enumerate(projects):
        projects[p] = update_description_from_github(project, user)
    return projects


def sort_projects(projects: list, by: str = "name") -> list:
    """Sorts the specified projects list by the specified key."""
    return sorted(projects, key=lambda x: x[by])


def get_projects(
    projects_path: str | Path,
    env_path: str | Path,
) -> list:
    """Gets and updates the project data from the specified JSON file."""

    # Load the local environment file if necessary
    if "GITHUB_API_TOKEN" not in os.environ:
        dotenv.load_dotenv(env_path)

    # Get secrets from environment variables
    github_token = os.environ["GITHUB_API_TOKEN"]

    # Read the projects JSON file
    projects = read_blueprint(projects_path)

    # Open a connection to the GitHub API and get the user's information
    g = github.Github(github_token)
    user = g.get_user()

    # Clean the projects data
    projects = clean_projects(projects, user)

    # Sort the projects by name
    projects = sort_projects(projects)

    # Return the projects data
    return projects


def get_tags(
    projects: list,
    remove_featured: bool = True,
    sort: bool = True,
) -> list:
    """Gets a list of tags from the specified projects list."""
    tags = {tag.lower() for project in projects for tag in project["tags"]}
    if remove_featured:
        tags.discard("featured")
    if sort:
        tags = sorted(tags)
    return list(tags)


def get_project_data(
    projects_path: str | Path,
    env_path: str | Path,
    as_dict: bool = False,
) -> tuple[list, list] | dict[str:list]:
    """Gets project and tag data from the specified JSON file.

    Essentially a wrapper for get_projects and get_tags.
    """
    projects = get_projects(projects_path, env_path)
    tags = get_tags(projects)
    if as_dict:
        return {"projects": projects, "tags": tags}
    return projects, tags

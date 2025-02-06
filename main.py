"""
The entry point for the Flask application.
"""

from pathlib import Path

from flask import Flask, render_template

from projects import PROJECTS_FILENAME, get_project_data

app = Flask(__name__)


@app.route("/")
def homepage():
    """Renders the homepage."""

    # Get the projects data
    project_data = get_project_data(
        projects_path=Path(f"./static/{PROJECTS_FILENAME}"),
        env_path=Path("./data/.env"),
        as_dict=True,
    )

    # Render the homepage with the pulled data
    return render_template(
        "index.html",
        **project_data,
        show_images=False,
    )


@app.route("/epicycler/")
def epicycler():
    """Renders the epicycler demo page."""
    return render_template("epicycler.html")


if __name__ == "__main__":
    app.run(debug=False)

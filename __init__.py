import json
import os

from flask import Flask, render_template, redirect, request

app = Flask(__name__)

@app.before_request
def force_https():
    if request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)

@app.route('/')
def homepage():
    projects_filename = os.path.join(app.static_folder, 'projects.json')
    with open(projects_filename) as projects_json:
        projects = json.load(projects_json)
    tags = {tag.lower() for project in projects.values() for tag in project['tags']}
    tags.discard('featured')
    return render_template(
        'index.html',
        projects=projects,
        tags=tags,
        show_images=False,
    )

@app.route('/epicycler/')
def epicycler():
    return render_template('epicycler.html')

if __name__ == '__main__':
    app.run(debug=False)
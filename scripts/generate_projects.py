import configparser
import json
import os
import pathlib

import github # pip3 install PyGithub

projects = {

    # Order of tags on website is controlled by order of tags here

    'Snake AI': {
        'tags': ['Featured', 'Machine Learning'],
        'image': '',
        'links': {
            'github': 'snake-ai',
        },
    },

    'Predicting Disaster Authenticity': {
        'tags': ['Featured', 'Machine Learning'],
        'image': '',
        'links': {
            'github': 'predicting-disaster-authenticity',
        },
    },

    'European Tweet Classification': {
        'tags': ['Featured', 'Machine Learning'],
        'image': '',
        'links': {
            'github': 'european-tweet-classification',
        },
    },

    'Demesstify': {
        'tags': ['Featured', 'Databases'],
        'image': '',
        'links': {
            'github': 'demesstify',
        },
    },

    'ManyMiles': {
        'tags': ['Featured', 'Web Dev', 'Databases'],
        'image': '',
        'links': {
            'github': 'manymiles',
            'preview': 'https://www.manymiles.app/',
        },
    },

    'GeoPhotos': {
        'tags': ['Featured'],
        'image': '',
        'links': {
            'github': 'geophotos',
        },
    },

    'EZPZ Plotting': {
        'tags': ['Software'],
        'image': '',
        'links': {
            'github': 'ezpz-plotting',
        },
    },

    'EZPZ Reducer': {
        'tags': ['Software'],
        'image': '',
        'links': {
            'github': 'ezpz-reducer',
        },
    },
    
    'Reddit Downloader': {
        'tags': ['Software'],
        'image': '',
        'links': {
            'github': 'reddit-downloader',
        },
    },
    
    'Specialty Referral Network': {
        'tags': ['Visualization', 'Web Dev'],
        'image': '',
        'links': {
            'github': 'referral-network',
        },
    },
    
    'Drawing Epicycler': {
        'tags': ['Web Dev'],
        'image': '',
        'links': {
            'github': 'drawing-epicycler',
            'preview': '/epicycler/',
        },
    },

    'Portfolio': {
        'tags': ['Web Dev'],
        'image': '',
        'links': {
            'github': 'portfolio',
            'preview': '/',
        },
    },

    'Cage Discord Bot': {
        'tags': ['Databases'],
        'image': '',
        'links': {
            'github': 'cage-discord-bot',
        },
    },

    'Bother Me Not': {
        'tags': [],
        'image': '',
        'links': {
            'github': 'bother-me-not',
        },
    },

    'Tooner': {
        'tags': [],
        'image': '',
        'links': {
            'github': 'tooner',
        },
    },

    'MultiTooner': {
        'tags': ['Software'],
        'image': '',
        'links': {
            'github': 'multitooner',
        },
    },

}

if __name__ == '__main__':
    SCRIPTS_FOLDER = pathlib.Path(__file__).resolve().parent
    PROJECT_FOLDER = SCRIPTS_FOLDER.parent
    STATIC_FOLDER = os.path.join(PROJECT_FOLDER, 'static')
    PROJECTS_FILE = os.path.join(STATIC_FOLDER, 'projects.json')

    DATA_FOLDER = os.path.join(PROJECT_FOLDER, 'data')
    CONFIG_FILE = os.path.join(DATA_FOLDER, 'config.ini')

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    g = github.Github(config['github']['token'])
    user = g.get_user()
    for project, info in projects.items():
        if 'links' in info and 'github' in info['links']:
            try:
                repository = user.get_repo(info['links']['github'])
                description = repository.description
            except github.GithubException:
                description = None
            info['description'] = description

    with open(PROJECTS_FILE, 'w') as output:
        json.dump(projects, output, indent=4)

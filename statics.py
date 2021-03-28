#!/usr/bin/python3

from helpers import read_ini, get_apikey

_statics = {
    'version': '1.0.4',
    'build': '005',
    'buffer_size': 4096,
    'config': read_ini('config.ini'),
    'apikey': get_apikey(),
    'allowed_paths': [
        'index.html',
        'favicon.ico',
        'css/index.css',
        'css/ConnectCode39.ttf',
        'js/i18-N.js',
        'js/index.js',
        'paper_template.html',
        'manager.html',
        'database/records.csv'
    ],
    'debug': True
}

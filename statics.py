#!/usr/bin/python3

from helpers import read_ini

_statics = {
    'version': '0.0.1',
    'build': '001',
    'buffer_size': 4096,
    'config': read_ini('config.ini'),
    'allowed_paths': [
        'index.html',
        'favicon.ico',
        'css/index.css',
        'css/ConnectCode39.ttf',
        'js/i18-N.js',
        'js/index.js',
        'paper_template.html',
        'manager.html'
    ],
    'debug': True
}

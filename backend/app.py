'''Entrypoint of the web service.
'''

from flask import Flask, send_from_directory


app = Flask(
    __name__,
    static_folder='build',
    static_url_path='/',
)


@app.route('/')
def index():
    '''Serve the index page.
    '''

    return send_from_directory(app.static_folder, 'index.html')

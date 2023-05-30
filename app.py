import flask
import DnD
import sqlite3



app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/players')
def listPlayers():
    con = sqlite3.connect('DM_Toolbox.db')
    cur = con.cursor()
    players = cur.execute('SELECT * FROM players')
    html = ''
    for player in players:
        html += f'<div class="btn "btn-primary>{}'



@app.route('/test')
def test():
    return 'This is a test'

app.run('0.0.0.0', debug=True)
import flask
import DnD
import sqlite3



app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template(
        'index.html',
        pageTitle = "DM's Toolbox"
        )

@app.route('/players')
def listPlayers():
    con = sqlite3.connect('DM_Toolbox.db')
    cur = con.cursor()
    try:
        players = cur.execute('SELECT * FROM players')
        html = ''
        # print(players.fetchone()[0])
        for player in players:
            html += f'''
            <a class="btn btn-primary" style="width: 100%;" href="/editPlayer/{player[0]}">
            Character name: {player[0]} |
            ac: {player[1]} |
            hp: {player[2]} 
            </a>'''
        con.close()
        return flask.render_template("players.html", pageTitle = "Player list", players = html)
    except sqlite3.OperationalError:
        con.close()
        return flask.render_template(
            "players.html", 
            players = "<div class='bg-danger'>No players in list! <a href='/newPlayer' class='btn btn-primary'>click here to create a new character</a></div>", 
            pageTitle = "Player list"
            )

@app.route('/newPlayer')
def newPlayer(): 
    return flask.render_template(
        "newPlayer.html",
        pageTitle = "Add new character"
        )

@app.route('/addPlayer', methods = ['POST', 'GET']) #The Backend
def addPlayer():

    name = flask.request.form['name']
    ac = flask.request.form['ac']
    hp = flask.request.form['hp']
    con = sqlite3.connect('DM_Toolbox.db')
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS players(name, ac, hp)')
    cur.execute(
        'INSERT INTO players VALUES(?, ?, ?)',
        [name, ac, hp]
    )
    con.commit()
    return flask.render_template("template.html", pageTitle = "SUCCESS, new character created!")

@app.route("/editPlayer/<name>")
def editPlayer(name):
    con = sqlite3.connect('DM_Toolbox.db')
    cur = con.cursor()
    try:
        players = cur.execute('SELECT * FROM players WHERE name = ?', [name])

        player = players.fetchone()

        player = f'''
        Character name: {player[0]}, 
        armor class: {player[1]}, 
        hit points: {player[2]} 
        <button 
        class="btn btn-danger" 
        onclick="confirm()">Delete character</button>
        <script>
        function confirm()
        </script>
        '''

        return flask.render_template("singlePlayer.html", pageTitle = name, player = player)
    except sqlite3.OperationalError as err:
        return(f"Big fail in sqlite query for {name}: {err}")
    
@app.route("/encounter")
def encounter():
    return("Add encounter screen")

@app.route('/test')
def test():
    return 'This is a test'

app.run('0.0.0.0', debug=True)
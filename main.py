# pip install flask
# pip install flask_mysql

from flask import Flask, render_template, request
from flaskext.mysql import MySQL

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# MySQL-Konfiguration
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config["MYSQL_DATABASE_USER"] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = "db_musikverwaltung"

mysql = MySQL(app)
mysql.init_app(app)


#################################################################################

@app.route('/alben')
def alben():
    # verbindung zur MySQLDatenbank herstellen
    cursor = mysql.get_db().cursor()

    # abfrage für sämtliche alben
    query = '''SELECT
			tbl_alben.*,
			tbl_interpreten.Interpret
			FROM tbl_alben
			INNER JOIN tbl_interpreten ON tbl_interpreten.IDInterpret=tbl_alben.FIDInterpret
			ORDER BY tbl_alben.Erscheinungsjahr DESC;
		'''

    cursor.execute(query)
    albums = cursor.fetchall()

    for i in albums:
        print(i)

    return render_template('alben.html', albums=albums)


#############################################################################################################

@app.route('/songtitel', methods=['GET', 'POST'])
def songtitel():
    # verbindung zur MySQLDatenbank herstellen
    cursor = mysql.get_db().cursor()

    # abfrage ob post daten für suche enthalten
    if request.method == 'POST':
        search_query = request.form['search']
        query = f'''SELECT tbl_songs.*,
                        tbl_alben.Albumtitel,
                        tbl_interpreten.Interpret
                    FROM tbl_songs
                    INNER JOIN tbl_alben on tbl_songs.FIDAlbum=tbl_alben.IDAlbum
                    INNER JOIN tbl_interpreten on tbl_interpreten.IDInterpret=tbl_alben.FIDInterpret
                    WHERE tbl_songs.Songtitel LIKE '%{search_query}%'
		'''
    else:
        # abfrage für sämtliche alben
        query = '''SELECT tbl_songs.*,
                        tbl_alben.Albumtitel,
                        tbl_interpreten.Interpret
                        FROM tbl_songs
                        INNER JOIN tbl_alben on tbl_songs.FIDAlbum=tbl_alben.IDAlbum
                        INNER JOIN tbl_interpreten on tbl_interpreten.IDInterpret=tbl_alben.FIDInterpret
                        ORDER BY Songtitel ASC;
		'''

    cursor.execute(query)
    songs = cursor.fetchall()

    for i in songs:
        print(i)

    return render_template('songtitel.html', songs=songs)


##############################################################################################################
@app.route('/interpreten')
def interpreten():
    # Verbindung zur Datenbank herstellen
    cursor = mysql.get_db().cursor()

    query = ''' SELECT tbl_interpreten.Interpret,tbl_alben.Albumtitel,tbl_alben.Erscheinungsjahr
                FROM tbl_interpreten
                inner JOIN tbl_alben on tbl_interpreten.IDInterpret = tbl_alben.FIDInterpret
                order by Erscheinungsjahr ASC;

    '''
    cursor.execute((query))
    interprets = cursor.fetchall()

    for i in interprets:
        print(i)

    return render_template('interpreten.html', interprets=interprets)


if __name__ == '__main__':
    app.run(debug=True)

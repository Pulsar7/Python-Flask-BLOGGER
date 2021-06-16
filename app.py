from flask import (render_template,send_from_directory,Flask,request,redirect)
import os,sqlite3
from datetime import datetime

global ALLE_ARTIKEL
ALLE_ARTIKEL = {}

class DATENBANK:
    def __init__(self):
        self.db_name = "DATA/BLOG.db"

    def create_table(self,table_name):
        verbindung = sqlite3.connect(self.db_name)
        database = verbindung.cursor()
        create_table_command = "CREATE TABLE IF NOT EXISTS"
        artikel_elem = "name,titel,beschreibung,content,zeitpunkt"
        artikel_table = "%s %s(%s)"%(create_table_command,table_name,artikel_elem)
        database.execute(artikel_table)
        verbindung.commit()
        verbindung.close()
        self.get_table_content(table_name)

    def insert_table_content(self,table,name,titel,beschreibung,content,creation_zeitpunkt):
        verbindung = sqlite3.connect(self.db_name)
        database = verbindung.cursor()
        insert_command = """INSERT INTO %s
                          (name, titel, beschreibung, content, zeitpunkt)
                          VALUES
                          ('%s','%s','%s','%s', '%s')"""%(table,name,titel,beschreibung,content,creation_zeitpunkt)
        database.execute(insert_command)
        verbindung.commit()
        verbindung.close()

    def get_table_content(self,table):
        verbindung = sqlite3.connect(self.db_name)
        database = verbindung.cursor()
        command = "SELECT * FROM %s"%(table)
        database.execute(command)
        rows = database.fetchall()
        return rows

    def get_element(self,table,element,element_name):
        verbindung = sqlite3.connect(self.db_name)
        database = verbindung.cursor()
        command = "SELECT * FROM %s WHERE %s='%s'"%(table,element_name,element)
        database.execute("%s"%(command))
        rows = database.fetchall()
        print(rows)
        verbindung.close()

    def create_datenbank(self):
        verbindung = sqlite3.connect(self.db_name)
        database = verbindung.cursor()
        verbindung.commit()
        verbindung.close()
        self.database = database
        self.create_table('ARTIKEL')

def datum():
    t = datetime.now()
    return ("%s.%s.1%s"%(t.day,t.month,t.year))

def uhrzeit():
    t = datetime.now()
    return ("%s:%s:%s Uhr"%(t.hour,t.minute,t.second))

app = Flask("MY BLOG",template_folder='templates',static_folder='static')

@app.route('/create')
def create():
    dateiname = "create.html"
    TITLE = "BLOG/HOME"
    regular_heading = "HEAD/regular_head.html"
    regular_footer = "FOOT/regular_footer.html"
    zeitpunkt = datum()
    return render_template(dateiname,title=TITLE,heading=regular_heading,
    footer=regular_footer,zeitpunkt=zeitpunkt)

@app.route('/create_article', methods=['POST','GET'])
def create_artikel():
    if (request.method == "POST"):
        form_data = request.form
        name = form_data.get('artikel_name')
        table = "ARTIKEL"
        titel = form_data.get('artikel_title')
        beschreibung = form_data.get('artikel_beschreibung')
        content = form_data.get('artikel_inhalt')
        creation_zeitpunkt = "%s - %s"%(uhrzeit(),datum())
        db.insert_table_content(table,name,titel,beschreibung,content,creation_zeitpunkt)
    return redirect('/create')

@app.route('/')
def index():
    TITLE = "MY-BLOG/HOME"
    file_path = "index.html"
    index_heading = "HEAD/index_head.html"
    index_footer = "FOOT/index_footer.html"
    rows = db.get_table_content('ARTIKEL')
    for row in rows:
        ALLE_ARTIKEL[row[0]] = {}
        ALLE_ARTIKEL[row[0]]['title'] = row[1]
        ALLE_ARTIKEL[row[0]]['beschreibung'] = row[2]
        ALLE_ARTIKEL[row[0]]['name'] = row[0]
        ALLE_ARTIKEL[row[0]]['weiterlesen_link'] = "/ARTIKEL/%s"%(row[0])
        ALLE_ARTIKEL[row[0]]['content'] = row[3]
        ALLE_ARTIKEL[row[0]]['creation_zeitpunkt'] = row[4]
        print(row)
    zeitpunkt = datum()
    return render_template(file_path,title=TITLE,
    index_heading=index_heading,ALLE_ARTIKEL=ALLE_ARTIKEL,
    index_footer=index_footer,zeitpunkt=zeitpunkt)

@app.route('/CSS/<name>')
def css(name):
    dateiname = "%s.css"%(name)
    return send_from_directory('static/CSS/',dateiname)

@app.route('/IMAGES/ARTIKEL/<name>')
def deckblatt_images(name):
    dateipfad = "static/IMAGES/ARTIKEL/%s/"%(name)
    dateiname = "deckblatt.jpg"
    return send_from_directory(dateipfad,dateiname)

@app.route('/ARTIKEL/<name>')
def artikel(name):
    dateipfad = "ARTIKEL/artikel.html"
    TITLE = ALLE_ARTIKEL[name]['title']
    content = ALLE_ARTIKEL[name]['content']
    creation_zeitpunkt = ALLE_ARTIKEL[name]['creation_zeitpunkt']
    return render_template(dateipfad,inhalt=content,title=TITLE,
    creation_zeitpunkt=creation_zeitpunkt)

if __name__ == '__main__':
    os.system("cls") #Windows
    HOST = '0.0.0.0'
    PORT = 80
    global db
    db = DATENBANK()
    db.create_datenbank()
    app.run(host=HOST,port=PORT,debug=True)

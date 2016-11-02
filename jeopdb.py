import csv, sqlite3

con = sqlite3.connect('jeopardy.sqlite')
con.text_factory = str
cur = con.cursor()
cur.execute('CREATE TABLE jeopardy (show INTEGER, date TEXT, round TEXT, category TEXT, value TEXT, question TEXT, answer TEXT, id integer PRIMARY KEY AUTOINCREMENT)')

with open('JEOPARDY_CSV.csv','rb') as jdata:
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(jdata) # comma is default delimiter
    to_db = [(i['show'], i['date'], i['round'], i['category'], i['value'], i['question'], i['answer']) for i in dr]

cur.executemany("INSERT INTO jeopardy (show, date, round, category, value, question, answer) VALUES (?, ?, ?, ?, ?, ?, ?);", to_db)
con.commit()

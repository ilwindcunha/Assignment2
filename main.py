from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import pypyodbc
#import sqlite3 as sql
import pyodbc
import datetime as DT
import csv
import os
import datetime


app = Flask(__name__)

import sqlite3

##################
server = 'ilwin.database.windows.net'
database = 'ilwin'
username = 'ilwin'
password = 'esxi@S5n'
driver = '{SQL Server}'
cnxn = pypyodbc.connect("Driver={ODBC Driver 13 for SQL Server};"
                        "Server=tcp:ilwin.database.windows.net;Database=ilwin;Uid=ilwin;Pwd=esxi@S5n;")
# cnxn = pyodbc.connect(
#     'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
cursor = cnxn.cursor()


@app.route('/')
def home():

   return render_template('index.php')

@app.route('/uploadCSV',methods=['POST'])
def uploadCSV():
    file = request.files['file']
    print(file.filename)
    #######
    destination = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    newfiledest = "/".join([destination, file.filename])
    file.save(newfiledest)
    #######
    with open(file.filename, encoding='ISO-8859-1') as f:
        reader = csv.reader(f)
        columns = next(reader)
        print(columns)
        query = 'insert into EarthquakeTwo ({0}) values ({1})'
        query = query.format(','.join(columns), ','.join('?' * len(columns)))

        for data in reader:
            cursor.execute(query, data)
            cursor.commit()

        m = os.path.getsize(newfiledest)

        return render_template('index.php', variable=m)


@app.route('/UI')
def UI():
    return render_template('view.html')


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    # print("here")

    if request.method == 'POST':
        # print("inside")
        query = "select count(*) from EarthquakeTwo where mag > 5.0"
        print(query)
        cursor.execute(query)
        result=cursor.fetchone()
        print("code here")
        print(result)
        value=result[0]
        print(value)

        return render_template("view.html", msg=value)

@app.route('/search', methods=['POST', 'GET'])
def search():
    # print("here")
    # Search    for 2.0 to 2.5, 2.5 to 3.0… for a week a day or the whole 30 days.
    if request.method == 'POST':
        # print("inside")
        rangeOne = request.form['range1']
        rangeTwo = request.form['range2']
        length = request.form['length']
        print(length)
        if(length=='week'):
            today = DT.date.today()
            criteria=today-DT.timedelta(days=7)
        if(length=='day'):
            today = DT.date.today()
            criteria = today - DT.timedelta(days=1)
        if(length=='month'):
            today = DT.date.today()
            criteria = today - DT.timedelta(days=30)

        print(today)
        print (criteria)


        # stringToday = today.dateutcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        # stringCriteria = criteria.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

        # query = "select * from EarthquakeTwo where (timee between "+today +" and "+criteria+") and (mag between '"+rangeTwo+"' and '"+rangeTwo+"')"
        query = "select * from EarthquakeTwo where timee between ? and ? "
        print(query)
        cursor.execute(query,(today,criteria))
        result=cursor.fetchone()
        print("code here")
        print(result)
        value=result[0]
        print(value)

        return render_template("view.html", msg=value)


if __name__ == '__main__':
   app.run(debug = True)
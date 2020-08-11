import os
from flask import Flask,redirect,render_template,request
import pyodbc
import time
import random
import urllib
import datetime
import json
import redis
import pickle
import hashlib

app = Flask(__name__)


#server = 'manietq.database.windows.net'
server = 'tcp:adbresourcegroup.database.windows.net'
database = 'adbdatabase'
username = 'bindhushreehr'
password = 'BinMay1!'
driver= '{ODBC Driver 13 for SQL Server}'
#myHostname = "adbresourcegroup.redis.cache.windows.net"
#myPassword = "aGqEGVxHVMtweNAOOvacdDuyTQcMpgu90vQSA8u3N8g="

r = redis.Redis(host='adns.redis.cache.windows.net',
        port=6380, db=0, password='bsNmTHHn7w6H+X4tPfgXp0pKwF8O7wUSERk9eq9y1U=', ssl=True)
   
def disdata():
   cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
   cursor = cnxn.cursor()
   start = time.time()
   cursor.execute("SELECT TOP 1000 * FROM [all_month]")
   row = cursor.fetchall()
   end = time.time()
   executiontime = end - start
   return render_template('searchearth.html', ci=row, t=executiontime)

def randrange(rangfro=None,rangto=None,num=None):
    dbconn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = dbconn.cursor()
    start = time.time()
    for i in range(0,int(num)):
        mag= round(random.uniform(rangfro, rangto),2)
        success="SELECT * from [all_month] where mag>'"+str(mag)+"'"
        hash = hashlib.sha224(success.encode('utf-8')).hexdigest()
        key = "redis_cache:" + hash
        if (r.get(key)):
           print("redis cached")
        else:
           # Do MySQL query   
           cursor.execute(success)
           data = cursor.fetchall()
           rows = []
           for j in data:
                rows.append(str(j))  
           # Put data into cache for 1 hour
           r.set(key, pickle.dumps(list(rows)) )
           r.expire(key, 36);
        cursor.execute(success)
    end = time.time()
    exectime = end - start
    return render_template('count.html', t=exectime)

@app.route('/')
def hello_world():
  return render_template('index.html')

@app.route('/displaydata', methods=['POST'])
def display():
    return disdata() 

@app.route('/multiplerun', methods=['GET'])
def randquery():
    rangfro = float(request.args.get('rangefrom'))
    rangto = float(request.args.get('rangeto'))
    num = request.args.get('nom')
    return randrange(rangfro,rangto,num) 	

if __name__ == '__main__':
  app.run()

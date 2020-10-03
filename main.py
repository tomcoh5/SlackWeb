from flask import Flask, render_template, request, redirect, session, request
from requests import get
import sqlite3
import time
import datetime
ip = get('https://api.ipify.org').text
app = Flask(__name__)

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#now = "2020-10-02 10:34:42"
def create_table():
    conn=sqlite3.connect("lite.db")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS MESSAGES (slack TEXT, timestamp TEXT)")
    conn.commit()
    conn.close()
def insert(message,time):
    conn=sqlite3.connect("lite.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO MESSAGES VALUES(?,?)",(message,time,))
    conn.commit()
    conn.close()
def p24():
    conn=sqlite3.connect("lite.db")
    cur=conn.cursor()
    let=cur.execute("SELECT * FROM MESSAGES WHERE timestamp >= datetime('now', '-1 day');")
    results = let.fetchall()
    conn.commit()
    conn.close()
    return results
def send_message_to_slack(text):
    from urllib import request
    import json

    post = {"text": "{0}".format(text)}

    try:
        json_data = json.dumps(post)
        req = request.Request("https://hooks.slack.com/services/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",
                              data=json_data.encode('ascii'),
                              headers={'Content-Type': 'application/json'})
        resp = request.urlopen(req)
    except Exception as em:
        print("EXCEPTION: " + str(em))
        


@app.route("/")
def home():
    create_table()

    return render_template('index.html')


@app.route("/slack")
def messagetoslack():
    return render_template("slack.html")


@app.route('/slack', methods=['POST', 'GET'])
def messageslackPost():
    global message
    message = request.form['text']
    send_message_to_slack(message)
    insert(message,now)
    return render_template("index.html")

@app.route("/p24")
def p24_page():
    new_p24 = p24()
    simple_string = " "
    new_list = list()
    for message, timestamps in new_p24:
        new_list.append(message + " sent at: " + timestamps + " \n ")
    new_list = ''.join(new_list)
    new_list = new_list.split('\n')
    return render_template("p24.html", message_24=new_list)



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)

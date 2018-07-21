import sqlite3
import time
import datetime
import pandas as pd
import random

dbName = 'dbData.db'

def create_table():
    conn = sqlite3.connect(dbName, timeout=10)
    cur = conn.cursor()
    #conn.execute('''DROP TABLE IF EXISTS users''')
    #conn.execute('''DROP TABLE IF EXISTS survey''')
    #conn.execute('''DROP TABLE IF EXISTS letter''')
    #conn.execute('''DROP TABLE IF EXISTS roundone''')
    #conn.execute('''DROP TABLE IF EXISTS roundtwo''')
    #conn.execute('''DROP TABLE IF EXISTS roundthree''')
    #conn.execute('''DROP TABLE IF EXISTS roundfour''')
    #conn.execute('''DROP TABLE IF EXISTS netincomedetails''')
    #conn.execute('''DROP TABLE IF EXISTS uniquecode''')
    conn.execute('''CREATE TABLE IF NOT EXISTS users (username,password, isActive, timestamp)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS survey (username,age, gender, highEducation,
                    live, area, role, income,isSurveyTaken, timestamp)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS letter (id, subid, letterdata)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS roundone (username, year, grossincome, reportedincome, 
                    incometax, grossincomelesstax, audited, fine, grossincomelesstaxlessfine, timestamp)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS roundtwo (username, year, grossincome, reportedincome, 
                    incometax, grossincomelesstax, audited, fine, grossincomelesstaxlessfine, timestamp)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS roundthree (username, year, grossincome, reportedincome, 
                    incometax, grossincomelesstax, audited, fine, grossincomelesstaxlessfine, timestamp)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS roundfour (username, year, grossincome, reportedincome, 
                    incometax, grossincomelesstax, audited, fine, grossincomelesstaxlessfine, timestamp)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS netincomedetails (id INTEGER PRIMARY KEY AUTOINCREMENT,username, netincomeR1, netincomeR2,netincomeR3,netincomeR4, finalnetincome,  timestamp)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS uniquecode (id INTEGER PRIMARY KEY AUTOINCREMENT,code, username)''')
    cur.close()
    conn.close()


#create_table()

def insert_user(username,password ):
    conn = sqlite3.connect(dbName, timeout=10)
    cur = conn.cursor()
    unix = time.time()
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%y-%m-%d %H:%M:%S'))
    print(date)
    isActive = 1
    sql = "SELECT username FROM users where username=?"
    cur.execute(sql, [(username)])
    hasUsername = cur.fetchall()
    print(hasUsername)
    if(len(hasUsername) > 0):
        result = "User exists"
        cur.close()
        conn.close()
        return result
    else:
        conn.execute('insert into users (username,password, isActive, timestamp) values (?,?,?,?)', (username,password,isActive,date))
        conn.commit()
        result = "User inserted"
        cur.close()
        conn.close()
        return result


def insert_survey(username, param1, param2, param3, param4, param5, param6, param7 ):
    conn = sqlite3.connect(dbName, timeout=10)
    cur = conn.cursor()
    unix = time.time()
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%y-%m-%d %H:%M:%S'))
    print(date)
    isSurveyTaken = 1
    conn.execute('insert into survey (username,age, gender, highEducation,live, area, role, income,isSurveyTaken, timestamp) values (?,?,?,?,?,?,?,?,?,?)',
                     (username,param1, param2, param3, param4, param5, param6,param7, isSurveyTaken,date))
    conn.commit()
    #sql = "SELECT username FROM users where username=?"
    #cur.execute(sql, [(username)])
    result = "User inserted"
    cur.close()
    conn.close()
    return result

def insert_roundOne(username, lstround1):
    try:
        conn = sqlite3.connect(dbName, timeout=10)
        cur = conn.cursor()
        unix = time.time()
        date = str(datetime.datetime.fromtimestamp(unix).strftime('%y-%m-%d %H:%M:%S'))

        for outerrow in lstround1:
            conn.execute(
                'insert into roundone (username,year, grossincome, reportedincome, incometax, grossincomelesstax, audited,fine, grossincomelesstaxlessfine,  timestamp) values (?,?,?,?,?,?,?,?,?,?)',
                (username, outerrow[0], outerrow[1], outerrow[2], outerrow[3], outerrow[4], outerrow[5], outerrow[6], outerrow[7],date))
            conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        error = e
        conn.rollback()
        cur.close()
        conn.close()
        return error

def insert_roundtwo(username, lstround2):
    try:
        conn = sqlite3.connect(dbName, timeout=10)
        cur = conn.cursor()
        unix = time.time()
        date = str(datetime.datetime.fromtimestamp(unix).strftime('%y-%m-%d %H:%M:%S'))

        for outerrow in lstround2:
            conn.execute(
                'insert into roundtwo (username,year, grossincome, reportedincome, incometax, grossincomelesstax, audited,fine, grossincomelesstaxlessfine,  timestamp) values (?,?,?,?,?,?,?,?,?,?)',
                (username, outerrow[0], outerrow[1], outerrow[2], outerrow[3], outerrow[4], outerrow[5], outerrow[6],
                 outerrow[7], date))
            conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        error = e
        conn.rollback()
        cur.close()
        conn.close()
        return error

def insert_roundthree(username, lstround3):
    try:
        conn = sqlite3.connect(dbName, timeout=10)
        cur = conn.cursor()
        unix = time.time()
        date = str(datetime.datetime.fromtimestamp(unix).strftime('%y-%m-%d %H:%M:%S'))

        for outerrow in lstround3:
            conn.execute(
                'insert into roundthree (username,year, grossincome, reportedincome, incometax, grossincomelesstax, audited,fine, grossincomelesstaxlessfine,  timestamp) values (?,?,?,?,?,?,?,?,?,?)',
                (username, outerrow[0], outerrow[1], outerrow[2], outerrow[3], outerrow[4], outerrow[5], outerrow[6],
                 outerrow[7], date))
            conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        error = e
        conn.rollback()
        cur.close()
        conn.close()
        return error


def insert_roundfour(username, lstround4):
    try:
        conn = sqlite3.connect(dbName, timeout=10)
        cur = conn.cursor()
        unix = time.time()
        date = str(datetime.datetime.fromtimestamp(unix).strftime('%y-%m-%d %H:%M:%S'))

        for outerrow in lstround4:
            conn.execute(
                'insert into roundfour (username,year, grossincome, reportedincome, incometax, grossincomelesstax, audited,fine, grossincomelesstaxlessfine,  timestamp) values (?,?,?,?,?,?,?,?,?,?)',
                (username, outerrow[0], outerrow[1], outerrow[2], outerrow[3], outerrow[4], outerrow[5], outerrow[6],
                 outerrow[7], date))
            conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        error = e
        conn.rollback()
        cur.close()
        conn.close()
        return error

def retrive_roundOne(username):
    conn = sqlite3.connect(dbName, timeout=10)
    cur = conn.cursor()
    sql = "SELECT * FROM roundone where username=?"
    cur.execute(sql, [(username)])
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users

def retrive_roundtwo(username):
    conn = sqlite3.connect(dbName, timeout=10)
    cur = conn.cursor()
    sql = "SELECT * FROM roundtwo where username=?"
    cur.execute(sql, [(username)])
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users

def retrive_roundthree(username):
    conn = sqlite3.connect(dbName, timeout=10)
    cur = conn.cursor()
    sql = "SELECT * FROM roundthree where username=?"
    cur.execute(sql, [(username)])
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users

def retrive_roundfour(username):
    conn = sqlite3.connect(dbName, timeout=10)
    cur = conn.cursor()
    sql = "SELECT * FROM roundfour where username=?"
    cur.execute(sql, [(username)])
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users

def rolback_ifNotComplete(username):
    conn = sqlite3.connect(dbName, timeout=10)
    cur = conn.cursor()
    selnetincome = "SELECT finalnetincome FROM netincomedetails where username=?"
    cur.execute(selnetincome, [(username)])
    result = cur.fetchall()
    if len(result) == 0:
        conn.execute(
            'delete from roundone where username=?', (username,))
        conn.execute(
            'delete from roundtwo where username=?', (username,))
        conn.execute(
            'delete from roundthree where username=?', (username,))
        conn.execute(
            'delete from roundfour where username=?', (username,))
        conn.commit()
    cur.close()
    conn.close()

def insert_finalnetincome(username):
    try:
        conn = sqlite3.connect(dbName, timeout=10)
        cur = conn.cursor()
        unix = time.time()
        date = str(datetime.datetime.fromtimestamp(unix).strftime('%y-%m-%d %H:%M:%S'))

        selR1 = "SELECT SUM(grossincomelesstaxlessfine) FROM roundone where username=?"
        cur.execute(selR1, [(username)])
        netincomeR1 = cur.fetchone()[0]
        selR2 = "SELECT SUM(grossincomelesstaxlessfine) FROM roundtwo where username=?"
        cur.execute(selR2, [(username)])
        netincomeR2 = cur.fetchone()[0]
        selR3 = "SELECT SUM(grossincomelesstaxlessfine) FROM roundthree where username=?"
        cur.execute(selR3, [(username)])
        netincomeR3 = cur.fetchone()[0]
        selR4 = "SELECT SUM(grossincomelesstaxlessfine) FROM roundfour where username=?"
        cur.execute(selR4, [(username)])
        netincomeR4 = cur.fetchone()[0]
        finalnetincome = float( netincomeR1) + float(netincomeR2) + float(netincomeR3) + float(netincomeR4)
        conn.execute(
            'insert into netincomedetails (username,netincomeR1, netincomeR2, netincomeR3, netincomeR4, finalnetincome,  timestamp) values (?,?,?,?,?,?,?)',
            (username,netincomeR1,netincomeR2, netincomeR3, netincomeR4 ,finalnetincome , date))
        conn.commit()

        selnetincome = "SELECT finalnetincome FROM netincomedetails where username=?"
        cur.execute(selnetincome, [(username)])
        result = cur.fetchone()[0]
        print("Thank god its done")
        cur.close()
        conn.close()
        return result
    except Exception as e:
        error = e
        conn.rollback()
        cur.close()
        conn.close()
        return error


def insert_letter():
    conn = sqlite3.connect(dbName, timeout=10)
    cur = conn.cursor()
    #conn.execute('''DELETE FROM letter''')
    conn.execute('insert into letter (id, subid, letterdata) values (?,?,?)',
                     (1, 1, "letter 1 (Control)"))
    conn.execute('insert into letter (id, subid, letterdata) values (?,?,?)',
                     (1, 1.1, "letter 1.1 (Control)"))
    conn.execute('insert into letter (id, subid, letterdata) values (?,?,?)',
                     (1, 1.2, "letter 1.2 (Control)"))
    conn.execute('insert into letter (id, subid, letterdata) values (?,?,?)',
                     (1, 1.3, "letter 1.3 (Control)"))
    conn.execute('insert into letter (id, subid, letterdata) values (?,?,?)',
                     (2, 2, "letter 2 (Social norm)"))
    conn.execute('insert into letter (id, subid, letterdata) values (?,?,?)',
                     (2, 2.1, "letter 2.1 (Social norm)"))
    conn.execute('insert into letter (id, subid, letterdata) values (?,?,?)',
                     (2, 2.2, "letter 2.2 (Social norm)"))
    conn.execute('insert into letter (id, subid, letterdata) values (?,?,?)',
                     (2, 2.3, "letter 2.3 (Social norm)"))
    conn.execute('insert into letter (id, subid, letterdata) values (?,?,?)',
                     (3, 3, "letter 3 (National pride)"))
    conn.execute('insert into letter (id, subid, letterdata) values (?,?,?)',
                     (3, 3.1, "letter 3.1 (National pride)"))
    conn.execute('insert into letter (id, subid, letterdata) values (?,?,?)',
                     (3, 3.2, "letter 3.2 (National pride)"))
    conn.execute('insert into letter (id, subid, letterdata) values (?,?,?)',
                     (3, 3.3, "letter 3.3 (National pride)"))
    conn.execute('insert into letter (id, subid, letterdata) values (?,?,?)',
                     (4, 4, "letter 4 (Deliberate choice)"))
    conn.execute('insert into letter (id, subid, letterdata) values (?,?,?)',
                     (4, 4.1, "letter 4.1 (Deliberate choice)"))
    conn.execute('insert into letter (id, subid, letterdata) values (?,?,?)',
                     (4, 4.2, "letter 4.2 (Deliberate choice)"))
    conn.execute('insert into letter (id, subid, letterdata) values (?,?,?)',
                     (4, 4.3, "letter 4.3 (Deliberate choice)"))
    conn.commit()
    cur.close()
    conn.close()

def insert_code():
    conn = sqlite3.connect(dbName, timeout=10)
    cur = conn.cursor()
    csvdata = '500_unique_codes.csv'
    df = pd.read_csv(csvdata)
    lstCode=[]
    for k in range(0, 499):
        lstCode.append(df.iloc[k, 0])
        k=k+1
    print(lstCode)

    for row in lstCode:
        val = str(row)
        conn.execute('insert into uniquecode (code, username) values (?,?)', (val,"nottaken"))
        conn.commit()
    cur.close()
    conn.close()

#insert_code()
#insert_letter()
#def drop_table():
    #conn = sqlite3.connect('/home/EconomicGame/mysite/dbData.db')
    #cur = conn.cursor()
    #conn.execute('''DROP TABLE roundone''')
    #print("Do not do this operation")
    #cur.close()
    #conn.close()
#drop_table()



def retrieve_user(username):
    conn = sqlite3.connect(dbName, timeout=10)
    cur = conn.cursor()
    sql = "SELECT username FROM users where username=?"
    cur.execute(sql, [(username)])
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users

def retrieve_code(username):
    conn = sqlite3.connect(dbName, timeout=10)
    cur = conn.cursor()
    tempuser = ''
    sql = "SELECT * FROM uniquecode where username = 'nottaken' ORDER BY RANDOM() LIMIT 1"
    cur.execute(sql)
    code = cur.fetchone()[1]
    print(code)
    conn.execute('update uniquecode set username = ? where code = ?', (username, code,))
    conn.commit()
    cur.close()
    conn.close()
    return code

#retrieve_code('pooja')

def retrieve_silumationDone(username):
    conn = sqlite3.connect(dbName, timeout=10)
    cur = conn.cursor()
    sql = "SELECT * FROM uniquecode where username=?"
    cur.execute(sql, [(username)])
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users

def retrieve_rank():
    conn = sqlite3.connect(dbName, timeout=10)
    cur = conn.cursor()
    sql = "SELECT * FROM netincomedetails order by finalnetincome desc"
    cur.execute(sql)
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users

def retrieve_survey(username):
    conn = sqlite3.connect(dbName, timeout=10)
    cur = conn.cursor()
    sql = "SELECT username FROM survey where username=?"
    cur.execute(sql, [(username)])
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users

def retrieve_letter(id):
    conn = sqlite3.connect(dbName, timeout=10)
    cur = conn.cursor()
    sql = "SELECT subid, letterdata FROM letter where id=?"
    cur.execute(sql, [(id)])
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users


print("Database operation complete")
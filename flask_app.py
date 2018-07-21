import sqlite3

from flask import Flask
from flask import Flask, flash, redirect, url_for, render_template, request, session, abort
import database as dbHandler
from random import randint
import json


app = Flask(__name__)
app.secret_key = "jake secret key"

dbHandler.create_table()

@app.route('/', methods=['POST', 'GET'])
@app.route('/register', methods=['POST', 'GET'])
def do_register():
    if request.method=='POST':
        username = str(request.form['username'])
        password = str(request.form['password'])
        confrmpassword = str(request.form['confirmpassword'])
        if(password == confrmpassword):
            result = dbHandler.insert_user(username, password)
            if result == "User inserted":
                user = dbHandler.retrieve_user(username)
                usrname = usrnameFormat(user)
                session['username'] = user
                return render_template('index.html', user = usrname)
            else:
                return render_template('register.html', userexists=result)
        else:
            error = "Password doesnot match"
            return render_template('register.html', error=error)
    else:
        return render_template('register.html')



@app.route('/login', methods=['POST', 'GET'])
def do_login():
    if request.method=='POST':
        username = str(request.form['name'])
        user = dbHandler.retrieve_user(username)
        if len(user)>0:
            session['username'] = user
            user_survey = dbHandler.retrieve_survey(username)
            usrname = usrnameFormat(user_survey)
            if len(user_survey)>0:
                isSimulationDone = dbHandler.retrieve_silumationDone(usrname)
                if len(isSimulationDone) > 0:
                    return render_template('simulationdone.html', user = usrname)
                else:
                    res = dbHandler.rolback_ifNotComplete(usrname)
                    return redirect(url_for('do_simulation'))
            else:
                session['username'] = user
                return redirect(url_for('index'))
        else:
            error = "NotValidUser"
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

@app.route('/index', methods=['POST', 'GET'])
def index():
    if request.method=='POST':
        if 'username' in session:
            username = session['username']
            usrname = usrnameFormat(username)
            age = str(request.form['age'])
            gender = str(request.form['gender'])
            edu = str(request.form['edu'])
            live = str(request.form['live'])
            area = str(request.form['area'])
            role = str(request.form['role'])
            income = str(request.form['income'])
            result = dbHandler.insert_survey(usrname,age, gender,edu, live,area,role,income)
            return render_template('simulation.html', user = usrname)
        else:
            sessionMsg = "sessionExpired"
            return render_template('login.html', sessionMsg=sessionMsg)
    else:
        if 'username' in session:
            username = session['username']
            usrname = usrnameFormat(username)
            print(usrname)
            user_survey = dbHandler.retrieve_survey(usrname)
            if len(user_survey) > 0:
                return redirect(url_for('do_simulation'))
            else:
                return render_template('index.html', user=usrname)
        else:
            sessionMsg = "sessionExpired"
            return render_template('login.html', sessionMsg=sessionMsg)

@app.route('/simulation', methods=['POST', 'GET'])
def do_simulation():
    if request.method=='POST':
        if 'username' in session:
            username = session['username']
            usrname = usrnameFormat(username)
            id = randint(1, 4)
            session['letterid'] = id
            getLetter(session['letterid'])
            #return redirect(url_for('summary'))
            return redirect(url_for('continueSimFirstAccept'))
        else:
            sessionMsg = "sessionExpired"
            return render_template('login.html', sessionMsg=sessionMsg)
    else:
        if 'username' in session:
            username = session['username']
            usrname = usrnameFormat(username)
            return render_template('simulation.html', user = usrname)
        else:
            sessionMsg = "sessionExpired"
            return render_template('login.html', sessionMsg=sessionMsg)

@app.route('/continueSimFirstAccept', methods=['POST', 'GET'])
def continueSimFirstAccept():
    if request.method == 'POST':
        if 'username' in session:
            username = session['username']
            usrname = usrnameFormat(username)
            return redirect(url_for('continue_simulationPageOne'))
        else:
            sessionMsg = "sessionExpired"
            return render_template('login.html', sessionMsg=sessionMsg)
    else:
        if 'username' in session:
            username = session['username']
            usrname = usrnameFormat(username)

            if 'letterchuncks' in session:
                letterchunks = session['letterchuncks']
                fltrid = letterchunks[0]
                print(fltrid)
                fltrdata = letterchunks[1]
                print(fltrdata)
                return render_template('continueSimFirstAccept.html', user=usrname, fltrid=fltrid,fltrdata= fltrdata )
        else:
            sessionMsg = "sessionExpired"
            return render_template('login.html', sessionMsg=sessionMsg)


@app.route('/continue_simulationPageOne', methods=['POST', 'GET'])
def continue_simulationPageOne():
    if request.method == 'POST':
        if 'username' in session:
            username = session['username']
            usrname = usrnameFormat(username)
            counter = str(request.form['ctnSim'])
            listRoundOne = []
            if(int(counter) < 11):
                counter=int(counter)+1
                taxrate = 0.25
                fine = 0.75
                grossIncome = str(request.form['grossIncome'])
                year = str(request.form['year'])
                grossIncome = float(grossIncome)
                year = int(year)
                reportedIncome = str(request.form['repIncome'])
                reportedIncome = float(reportedIncome)
                incomeTax = reportedIncome*taxrate
                grossIncomeLessTax = grossIncome - incomeTax
                audited=getAudited()
                rowFine=0
                grossIncomeLessTaxLessFine = 0
                if audited=='YES':
                    if reportedIncome < grossIncome:
                        rowFine = (grossIncome-reportedIncome)*fine
                        grossIncomeLessTaxLessFine= (grossIncome*(1-0.25))-rowFine
                    else:
                        grossIncomeLessTaxLessFine = grossIncomeLessTax
                else:
                    grossIncomeLessTaxLessFine = grossIncomeLessTax
                templst=[]
                for row in range(year, year+1):
                    templst.append(year)
                    templst.append(grossIncome)
                    templst.append(reportedIncome)
                    templst.append(incomeTax)
                    templst.append(grossIncomeLessTax)
                    templst.append(audited)
                    templst.append(rowFine)
                    templst.append(grossIncomeLessTaxLessFine)
                    listRoundOne.append(templst)
                print(counter)
                result = dbHandler.insert_roundOne(usrname, listRoundOne)
                listRoundOne = dbHandler.retrive_roundOne(usrname)
                netIncome = 0
                for element in listRoundOne:
                    tempnum = element[8]
                    netIncome=netIncome+tempnum

                listGetRoundone=[]
                return render_template('continue_simulationPageOne.html', user=usrname, listRoundOne=listRoundOne, listGetRoundone=listGetRoundone, counter=counter, netIncome=netIncome)
            else:
                return redirect(url_for('continueSimSecondAccept'))
        else:
            sessionMsg = "sessionExpired"
            return render_template('login.html', sessionMsg=sessionMsg)
    else:
        if 'username' in session:
            username = session['username']
            usrname = usrnameFormat(username)
            year = 1
            grossIncome = 59000
            repIncome = 0
            counter=1
            listGetRoundone=[]
            templst = []
            for row in range(year, year + 1):
                templst.append(usrname)
                templst.append(year)
                templst.append(grossIncome)
                listGetRoundone.append(templst)
            print(listGetRoundone)
            return render_template('continue_simulationPageOne.html', user=usrname, listRoundOne=listGetRoundone, counter=counter)
        else:
            sessionMsg = "sessionExpired"
            return render_template('login.html', sessionMsg=sessionMsg)



@app.route('/continueSimSecondAccept', methods=['POST', 'GET'])
def continueSimSecondAccept():
    if request.method == 'POST':
        if 'username' in session:
            username = session['username']
            usrname = usrnameFormat(username)
            return redirect(url_for('continue_simulationPageTwo'))
        else:
            sessionMsg = "sessionExpired"
            return render_template('login.html', sessionMsg=sessionMsg)
    else:
        if 'username' in session:
            username = session['username']
            usrname = usrnameFormat(username)
            if 'letterchuncks' in session:
                letterchunks = session['letterchuncks']
                fltrid = letterchunks[2]
                print(fltrid)
                fltrdata = letterchunks[3]
                print(fltrdata)
                return render_template('continueSimSecondAccept.html', user=usrname, fltrid=fltrid,fltrdata= fltrdata )
        else:
            sessionMsg = "sessionExpired"
            return render_template('login.html', sessionMsg=sessionMsg)


@app.route('/continue_simulationPageTwo', methods=['POST', 'GET'])
def continue_simulationPageTwo():
    if request.method == 'POST':
        if 'username' in session:
            username = session['username']
            usrname = usrnameFormat(username)
            counter = str(request.form['ctnSim'])
            listRoundTwo = []
            if(int(counter) < 11):
                counter=int(counter)+1
                taxrate = 0.25
                fine = 1
                grossIncome = str(request.form['grossIncome'])
                year = str(request.form['year'])
                grossIncome = float(grossIncome)
                year = int(year)
                reportedIncome = str(request.form['repIncome'])
                reportedIncome = float(reportedIncome)
                incomeTax = reportedIncome*taxrate
                grossIncomeLessTax = grossIncome - incomeTax
                audited=getAudited()
                grossIncomeLessTaxLessFine = 0
                rowFine=0
                if audited == 'YES':
                    if reportedIncome < grossIncome:
                        rowFine = (grossIncome - reportedIncome) * fine
                        grossIncomeLessTaxLessFine = (grossIncome * (1 - 0.25)) - rowFine
                    else:
                        grossIncomeLessTaxLessFine = grossIncomeLessTax
                else:
                    grossIncomeLessTaxLessFine = grossIncomeLessTax
                templst=[]
                for row in range(year, year+1):
                    templst.append(year)
                    templst.append(grossIncome)
                    templst.append(reportedIncome)
                    templst.append(incomeTax)
                    templst.append(grossIncomeLessTax)
                    templst.append(audited)
                    templst.append(rowFine)
                    templst.append(grossIncomeLessTaxLessFine)
                    listRoundTwo.append(templst)
                result = dbHandler.insert_roundtwo(usrname, listRoundTwo)
                listRoundTwo = dbHandler.retrive_roundtwo(usrname)
                netIncome = 0
                for element in listRoundTwo:
                    tempnum = element[8]
                    netIncome=netIncome+tempnum
                listGetRoundone=[]
                print(listRoundTwo)
                return render_template('continue_simulationPageTwo.html', user=usrname, listRoundTwo=listRoundTwo, listGetRoundone=listGetRoundone, counter=counter, netIncome=netIncome)
            else:
                return redirect(url_for('continueSimThirdAccept'))
        else:
            sessionMsg = "sessionExpired"
            return render_template('login.html', sessionMsg=sessionMsg)
    else:
        if 'username' in session:
            username = session['username']
            usrname = usrnameFormat(username)
            year = 1
            grossIncome = 59000
            repIncome = 0
            counter=1
            listRoundTwo=[]
            templst = []
            for row in range(year, year + 1):
                templst.append(usrname)
                templst.append(year)
                templst.append(grossIncome)
                listRoundTwo.append(templst)
            print(listRoundTwo)
            return render_template('continue_simulationPageTwo.html', user=usrname, listRoundTwo=listRoundTwo, counter=counter)
        else:
            sessionMsg = "sessionExpired"
            return render_template('login.html', sessionMsg=sessionMsg)



@app.route('/continueSimThirdAccept', methods=['POST', 'GET'])
def continueSimThirdAccept():
    if request.method == 'POST':
        if 'username' in session:
            username = session['username']
            usrname = usrnameFormat(username)
            return redirect(url_for('continue_simulationPageThree'))
        else:
            sessionMsg = "sessionExpired"
            return render_template('login.html', sessionMsg=sessionMsg)
    else:
        if 'username' in session:
            username = session['username']
            usrname = usrnameFormat(username)
            if 'letterchuncks' in session:
                letterchunks = session['letterchuncks']
                fltrid = letterchunks[4]
                print(fltrid)
                fltrdata = letterchunks[5]
                print(fltrdata)
                return render_template('continueSimThirdAccept.html', user=usrname, fltrid=fltrid,fltrdata= fltrdata )
        else:
            sessionMsg = "sessionExpired"
            return render_template('login.html', sessionMsg=sessionMsg)



@app.route('/continue_simulationPageThree', methods=['POST', 'GET'])
def continue_simulationPageThree():
    if request.method == 'POST':
        if 'username' in session:
            username = session['username']
            usrname = usrnameFormat(username)
            counter = str(request.form['ctnSim'])
            listRoundThree=[]
            if(int(counter) < 11):
                counter=int(counter)+1
                taxrate = 0.50
                fine = 0.75
                grossIncome = str(request.form['grossIncome'])
                year = str(request.form['year'])
                grossIncome = float(grossIncome)
                year = int(year)
                reportedIncome = str(request.form['repIncome'])
                reportedIncome = float(reportedIncome)
                incomeTax = reportedIncome*taxrate
                grossIncomeLessTax = grossIncome - incomeTax
                audited=getAudited()
                grossIncomeLessTaxLessFine = 0
                rowFine=0
                if audited == 'YES':
                    if reportedIncome < grossIncome:
                        rowFine = (grossIncome - reportedIncome) * fine
                        grossIncomeLessTaxLessFine = (grossIncome * (1 - 0.50)) - rowFine
                    else:
                        grossIncomeLessTaxLessFine = grossIncomeLessTax
                else:
                    grossIncomeLessTaxLessFine = grossIncomeLessTax
                templst=[]
                for row in range(year, year+1):
                    templst.append(year)
                    templst.append(grossIncome)
                    templst.append(reportedIncome)
                    templst.append(incomeTax)
                    templst.append(grossIncomeLessTax)
                    templst.append(audited)
                    templst.append(rowFine)
                    templst.append(grossIncomeLessTaxLessFine)
                    listRoundThree.append(templst)
                result = dbHandler.insert_roundthree(usrname, listRoundThree)
                listRoundThree = dbHandler.retrive_roundthree(usrname)
                netIncome = 0
                for element in listRoundThree:
                    tempnum = element[8]
                    netIncome=netIncome+tempnum
                listGetRoundone=[]
                print(listRoundThree)
                return render_template('continue_simulationPageThree.html', user=usrname, listRoundThree=listRoundThree, listGetRoundone=listGetRoundone, counter=counter, netIncome=netIncome)
            else:
                return redirect(url_for('continueSimFourthAccept'))
        else:
            sessionMsg = "sessionExpired"
            return render_template('login.html', sessionMsg=sessionMsg)
    else:
        if 'username' in session:
            username = session['username']
            usrname = usrnameFormat(username)
            year = 1
            grossIncome = 59000
            repIncome = 0
            counter=1
            listRoundThree=[]
            templst = []
            for row in range(year, year + 1):
                templst.append(usrname)
                templst.append(year)
                templst.append(grossIncome)
                listRoundThree.append(templst)
            print(listRoundThree)
            return render_template('continue_simulationPageThree.html', user=usrname, listRoundThree=listRoundThree, counter=counter)
        else:
            sessionMsg = "sessionExpired"
            return render_template('login.html', sessionMsg=sessionMsg)



@app.route('/continueSimFourthAccept', methods=['POST', 'GET'])
def continueSimFourthAccept():
    if request.method == 'POST':
        if 'username' in session:
            username = session['username']
            usrname = usrnameFormat(username)
            return redirect(url_for('continue_simulationPageFour'))
        else:
            sessionMsg = "sessionExpired"
            return render_template('login.html', sessionMsg=sessionMsg)
    else:
        if 'username' in session:
            username = session['username']
            usrname = usrnameFormat(username)
            if 'letterchuncks' in session:
                letterchunks = session['letterchuncks']
                fltrid = letterchunks[6]
                print(fltrid)
                fltrdata = letterchunks[7]
                print(fltrdata)
                return render_template('continueSimFourthAccept.html', user=usrname, fltrid=fltrid,fltrdata= fltrdata )
        else:
            sessionMsg = "sessionExpired"
            return render_template('login.html', sessionMsg=sessionMsg)



@app.route('/continue_simulationPageFour', methods=['POST', 'GET'])
def continue_simulationPageFour():
    if request.method == 'POST':
        if 'username' in session:
            username = session['username']
            usrname = usrnameFormat(username)
            counter = str(request.form['ctnSim'])
            listRoundFour=[]
            if(int(counter) < 11):
                counter=int(counter)+1
                taxrate = 0.50
                fine = 1
                grossIncome = str(request.form['grossIncome'])
                year = str(request.form['year'])
                grossIncome = float(grossIncome)
                year = int(year)
                reportedIncome = str(request.form['repIncome'])
                reportedIncome = float(reportedIncome)
                incomeTax = reportedIncome*taxrate
                grossIncomeLessTax = grossIncome - incomeTax
                audited=getAudited()
                grossIncomeLessTaxLessFine = 0
                rowFine=0
                if audited == 'YES':
                    if reportedIncome < grossIncome:
                        rowFine = (grossIncome - reportedIncome) * fine
                        grossIncomeLessTaxLessFine = (grossIncome * (1 - 0.50)) - rowFine
                    else:
                        grossIncomeLessTaxLessFine = grossIncomeLessTax
                else:
                    grossIncomeLessTaxLessFine = grossIncomeLessTax
                templst=[]
                for row in range(year, year+1):
                    templst.append(year)
                    templst.append(grossIncome)
                    templst.append(reportedIncome)
                    templst.append(incomeTax)
                    templst.append(grossIncomeLessTax)
                    templst.append(audited)
                    templst.append(rowFine)
                    templst.append(grossIncomeLessTaxLessFine)
                    listRoundFour.append(templst)
                result = dbHandler.insert_roundfour(usrname, listRoundFour)
                listRoundFour = dbHandler.retrive_roundfour(usrname)
                netIncome = 0
                for element in listRoundFour:
                    tempnum = element[8]
                    netIncome=netIncome+tempnum
                listGetRoundone=[]
                print(listRoundFour)
                return render_template('continue_simulationPageFour.html', user=usrname, listRoundFour=listRoundFour, listGetRoundone=listGetRoundone, counter=counter, netIncome=netIncome)
            else:
                return redirect(url_for('summary'))
        else:
            sessionMsg = "sessionExpired"
            return render_template('login.html', sessionMsg=sessionMsg)
    else:
        if 'username' in session:
            username = session['username']
            usrname = usrnameFormat(username)
            year = 1
            grossIncome = 59000
            repIncome = 0
            counter=1
            listRoundFour=[]
            templst = []
            for row in range(year, year + 1):
                templst.append(usrname)
                templst.append(year)
                templst.append(grossIncome)
                listRoundFour.append(templst)
            print(listRoundFour)
            return render_template('continue_simulationPageFour.html', user=usrname, listRoundFour=listRoundFour, counter=counter)
        else:
            sessionMsg = "sessionExpired"
            return render_template('login.html', sessionMsg=sessionMsg)


@app.route('/summary', methods=['POST', 'GET'])
def summary():
    if request.method == 'POST':
        if 'username' in session:
            username = session['username']
            usrname = usrnameFormat(username)
            uniquecode = dbHandler.retrieve_code(usrname)
            return render_template('goodbye.html', user=usrname, uniquecode=uniquecode)
        else:
            sessionMsg = "sessionExpired"
            return render_template('login.html', sessionMsg=sessionMsg)
    else:
        if 'username' in session:
            username = session['username']
            usrname = usrnameFormat(username)
            #tmp1 = [[1, 59000, 11, 2.75, 58997.25, 'no', 0, 59000], [2, 59100, 11, 2.75, 59097.25, 'no', 0, 59100], [3, 59200, 11, 2.75, 59197.25, 'no', 0, 59200], [4, 59300, 11, 2.75, 59297.25, 'no', 0, 59300], [5, 59400, 11, 2.75, 59397.25, 'no', 0, 59400], [6, 59500, 11, 2.75, 59497.25, 'no', 0, 59500], [7, 59600, 11, 2.75, 59597.25, 'no', 0, 59600], [8, 59700, 11, 2.75, 59697.25, 'no', 0, 59700], [9, 59800, 11, 2.75, 59797.25, 'no', 0, 59800], [10, 59900, 11, 2.75, 59897.25, 'no', 0, 59900]]
            #tmp2 = [[1, 59000, 11, 2.75, 58997.25, 'no', 0, 59000], [2, 59100, 11, 2.75, 59097.25, 'no', 0, 59100], [3, 59200, 11, 2.75, 59197.25, 'no', 0, 59200], [4, 59300, 11, 2.75, 59297.25, 'no', 0, 59300], [5, 59400, 11, 2.75, 59397.25, 'no', 0, 59400], [6, 59500, 11, 2.75, 59497.25, 'no', 0, 59500], [7, 59600, 11, 2.75, 59597.25, 'no', 0, 59600], [8, 59700, 11, 2.75, 59697.25, 'no', 0, 59700], [9, 59800, 11, 2.75, 59797.25, 'no', 0, 59800], [10, 59900, 11, 2.75, 59897.25, 'no', 0, 59900]]
            #tmp3 = [[1, 59000, 11, 2.75, 58997.25, 'no', 0, 59000], [2, 59100, 11, 2.75, 59097.25, 'no', 0, 59100], [3, 59200, 11, 2.75, 59197.25, 'no', 0, 59200], [4, 59300, 11, 2.75, 59297.25, 'no', 0, 59300], [5, 59400, 11, 2.75, 59397.25, 'no', 0, 59400], [6, 59500, 11, 2.75, 59497.25, 'no', 0, 59500], [7, 59600, 11, 2.75, 59597.25, 'no', 0, 59600], [8, 59700, 11, 2.75, 59697.25, 'no', 0, 59700], [9, 59800, 11, 2.75, 59797.25, 'no', 0, 59800], [10, 59900, 11, 2.75, 59897.25, 'no', 0, 59900]]
            #tmp4 = [[1, 59000, 11, 2.75, 58997.25, 'no', 0, 59000], [2, 59100, 11, 2.75, 59097.25, 'no', 0, 59100], [3, 59200, 11, 2.75, 59197.25, 'no', 0, 59200], [4, 59300, 11, 2.75, 59297.25, 'no', 0, 59300], [5, 59400, 11, 2.75, 59397.25, 'no', 0, 59400], [6, 59500, 11, 2.75, 59497.25, 'no', 0, 59500], [7, 59600, 11, 2.75, 59597.25, 'no', 0, 59600], [8, 59700, 11, 2.75, 59697.25, 'no', 0, 59700], [9, 59800, 11, 2.75, 59797.25, 'no', 0, 59800], [10, 59900, 11, 2.75, 59897.25, 'no', 0, 59900]]
            #result = insertRound(usrname, tmp1, tmp2, tmp3, tmp4 )
            result = dbHandler.insert_finalnetincome(usrname)
            print(result)
            lstrank = dbHandler.retrieve_rank()
            print(lstrank)
            rank = 0
            id = 0
            for row in lstrank:
                id=id+1
                if row[1] == usrname:
                    rank = id
                    break
            return render_template('summary.html', user=usrname, netincome=result, rank=rank)
        else:
            sessionMsg = "sessionExpired"
            return render_template('login.html', sessionMsg=sessionMsg)


def insertRound(username, listRoundOne, listRoundTwo, listRoundThree, listRoundFour):
    result = dbHandler.insert_round(username, listRoundOne, listRoundTwo, listRoundThree, listRoundFour)
    print(result)
    return result

def usrnameFormat(username):
    usrname = ''
    for row in username:
        usrname = row[0]
    print(str(usrname))
    return usrname

def getLetter(id):
    letterlist = dbHandler.retrieve_letter(id)
    i = 0
    letterchunks = []
    if len(letterlist) > 0:
        for row in letterlist:
            for _row in row:
                    print(_row)
                    letterchunks.append(str(_row))
                    i = i + 1
    session['letterchuncks'] = letterchunks
    print(letterchunks)
    return letterchunks

def getAudited():
    id = randint(1, 15)
    isAugdit='NO'
    #id = 14
    if id == 14 :
        isAugdit='YES'
    return isAugdit

def cleanfloat(var):
    print(var)
    if var == '#REF!' or var == '-' or var == 'nan':
        var = 0
    if type(var) != float:
        var = float(var.replace(',',''))
    return var

@app.route('/logout')
def do_logout():
    if 'username' in session:
        username = session['username']
        usrname = usrnameFormat(username)
        result = dbHandler.rolback_ifNotComplete(usrname)
        session.pop('username', None)
        session.pop('letterid', None)
        session.pop('letterchuncks', None)
        return  render_template('login.html')
    else:
        return  render_template('login.html')


if __name__ == "__main__":
    app.run()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(dbHandler, '_database', None)

@app.errorhandler(500)
def internal_error_500(e):
    error = str(e)
    return render_template('error500.html', error=error)
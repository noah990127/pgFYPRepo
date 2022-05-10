import os
from flask import Blueprint,render_template, request, redirect, url_for
from app.models.base import db
from app.models.admin import Admin
from app.models.student import Student
from app.models.order import Order
from app.models.seat import Seat
from sqlalchemy import or_,and_,all_,any_

adminBP = Blueprint('Admin',__name__)

# set save path
save_path = os.path.join(os.path.dirname(__file__),'export_file')

@adminBP.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('adminLogin.html')
    else:
        # 获取姓名密码
        staffID = request.form.get('staffID')
        _password = request.form.get('password')
        loginResult = Admin.query.filter(and_(Admin.id == staffID, Admin._password == _password)).first()
        if loginResult:
            global staffSeq
            staffSeq = staffID
            return redirect(url_for('Admin.adminPage'))
        else:
            return render_template('adminLogin.html', error_msg = 'The staff ID or the password must be wrong, please try again.')

@adminBP.route('/adminPage', methods=['GET','POST'])
def adminPage():
    if request.method == 'GET':
        order = Order.query.all()
        infoList = []
        for eachOrder in order:
            temp = []

            stuID = eachOrder.stuID
            sID = eachOrder.sID

            student = Student.query.filter(Student.stuID == stuID).first()
            seat = Seat.query.filter(Seat.sID == sID).first()

            temp.append(stuID)
            temp.append(student.name)
            temp.append(sID)
            temp.append(seat.floor)
            temp.append(eachOrder.time)
            temp.append(eachOrder.status)
            temp.append(eachOrder.recordID)
            infoList.append(temp)

        loginResult = Admin.query.filter(and_(Admin.id == staffSeq)).first()
        return render_template('adminHomepage.html', name = loginResult.name, infoList = infoList, visible = 1)
    else:
        sIDtemp = request.form.get('sID')
        sID = int(sIDtemp)
        seat = Seat.query.filter(Seat.sID == sID).first()
        order = Order.query.filter(and_(Order.sID == sID,Order.status == 0)).first()
        temp = []
        stuID = order.stuID
        sID = order.sID
        student = Student.query.filter(Student.stuID == stuID).first()
        seat = Seat.query.filter(Seat.sID == sID).first()

        temp.append(stuID)
        temp.append(student.name)
        temp.append(sID)
        temp.append(seat.floor)
        temp.append(order.time)
        temp.append(order.status)
        temp.append(order.recordID)

        loginResult = Admin.query.filter(and_(Admin.id == staffSeq)).first()

        return render_template('adminHomepage.html', name = loginResult.name, infoList = temp, visible = 0)


@adminBP.route('/deleteRecord/<recordID>/', methods=['GET'])
def deleteRecord(recordID):
    if request.method == 'GET':
        with db.auto_commit():
            order = Order.query.filter(Order.recordID == recordID).first()
            sID = order.sID
            db.session.delete(order)

            seat = Seat.query.filter(Seat.sID == sID).first()
            seat.status = 0 # released

        order = Order.query.all() 
        infoList = []
        for eachOrder in order:
            temp = []

            stuID = eachOrder.stuID
            sID = eachOrder.sID

            student = Student.query.filter(Student.stuID == stuID).first()
            seat = Seat.query.filter(Seat.sID == sID).first()

            temp.append(stuID)
            temp.append(student.name)
            temp.append(sID)
            temp.append(seat.floor)
            temp.append(eachOrder.time)
            temp.append(eachOrder.status)
            temp.append(eachOrder.recordID)

            infoList.append(temp)

        loginResult = Admin.query.filter(and_(Admin.id == staffSeq)).first()
        return render_template('adminHomepage.html', name = loginResult.name, infoList = infoList, msg = "Successfully deleted.")

@adminBP.route('/updateBlacklist', methods=['GET','POST'])
def updateBlacklist():
    if request.method == 'GET':
        loginResult = Admin.query.filter(and_(Admin.id == staffSeq)).first()
        student = Student.query.filter(Student.confidency == 0).all()
        infoList = []
        for each in student:
            temp = []
            temp.append(each.stuID)
            temp.append(each.name)
            infoList.append(temp)
        return render_template('blacklist.html', name = loginResult.name, infoList = infoList, visible = 1)
    else:
        stuIDtemp = request.form.get('stuID')
        stuID = int(stuIDtemp)
        student = Student.query.filter(and_(Student.stuID == stuID,Student.confidency == 0)).first()
        temp = []
        msg = ""
        if student:
            temp.append(student.stuID)
            temp.append(student.name)
        else:
            msg = "Not found."
        loginResult = Admin.query.filter(and_(Admin.id == staffSeq)).first()
        return render_template('blacklist.html', name = loginResult.name, infoList = temp, visible = 0, msg = msg)        

@adminBP.route('/removeBlacklist/<stuID>/', methods=['GET'])
def removeBlacklist(stuID):
    if request.method == 'GET':
        loginResult = Admin.query.filter(and_(Admin.id == staffSeq)).first()

        with db.auto_commit():
            student = Student.query.filter(Student.stuID == stuID).first()
            student.confidency = 1 # booked

        student = Student.query.filter(Student.confidency == 0).all()
        infoList = []
        for each in student:
            temp = []
            temp.append(each.stuID)
            temp.append(each.name)
            infoList.append(temp)

        return render_template('blacklist.html', name = loginResult.name, infoList = infoList, msg = "Successfully removed.")

@adminBP.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'GET':
        usename = None
        return redirect(url_for('Admin.login'))


@adminBP.route('/studentOverview', methods=['GET','POST'])
def studentOverview():
    if request.method == 'GET':
        loginResult = Admin.query.filter(and_(Admin.id == staffSeq)).first()
        student = Student.query.filter(Student.confidency == 1).all()
        infoList = []
        for each in student:
            temp = []
            temp.append(each.stuID)
            temp.append(each.name)
            infoList.append(temp)
        return render_template('allStudentList.html', name = loginResult.name, infoList = infoList, visible = 1)
    else:
        stuIDtemp = request.form.get('stuID')
        stuID = int(stuIDtemp)
        student = Student.query.filter(and_(Student.stuID == stuID,Student.confidency == 1)).first()
        temp = []
        msg = ""
        if student:
            temp.append(student.stuID)
            temp.append(student.name)
        else:
            msg = "Not found."
        loginResult = Admin.query.filter(and_(Admin.id == staffSeq)).first()
        return render_template('allStudentList.html', name = loginResult.name, infoList = temp, visible = 0, msg = msg)  

@adminBP.route('/addToBlackList/<stuID>/', methods=['GET'])
def addToBlackList(stuID):
    if request.method == 'GET':
        loginResult = Admin.query.filter(and_(Admin.id == staffSeq)).first()

        with db.auto_commit():
            student = Student.query.filter(Student.stuID == stuID).first()
            student.confidency = 0 # booked

        student = Student.query.filter(Student.confidency == 0).all()
        infoList = []
        for each in student:
            temp = []
            temp.append(each.stuID)
            temp.append(each.name)
            infoList.append(temp)

        return render_template('allStudentList.html', name = loginResult.name, infoList = infoList, msg = "Successfully added.")


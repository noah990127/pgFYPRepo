from flask import Blueprint,render_template, request, redirect, url_for
from app.models.base import db
from app.models.student import Student
from app.models.order import Order
from app.models.seat import Seat
from sqlalchemy import or_,and_,all_,any_
import qrcode as qr
import time
import cv2
from pyzbar import pyzbar
import csv

studentBP = Blueprint('Student',__name__)

#注册
@studentBP.route('/register', methods=['GET','POST'])
def visitoradmin():
	if request.method == 'GET':
		return render_template('registration.html')
	else:
		_id= request.form.get('_id')
		name=request.form.get('name')
		pw=request.form.get('pw')
		pw1=request.form.get('pw1')
		pnumber=request.form.get('pnumber')
		loginResult = Student.query.filter(Student.stuID == _id).first()
		if loginResult:
			return render_template('registration.html', error_msg = 'The student ID has been already registered.')
		if pw!=pw1:
			return render_template('registration.html', error_msg = 'Please confirm your password again.')
		else:
			with db.auto_commit():
				student = Student()
				student.stuID = _id
				student.name = name
				student._password = pw
				student.teleNum = pnumber
				student.confidency = 1
				db.session.add(student)
			return render_template('registration.html', msg = 'Successfully resgistered, click here to sign in.')

@studentBP.route('/visitorlogin', methods=['GET','POST'])
def visitorlogin():
	if request.method == 'GET':
		return render_template('studentLogin.html')
	else:
		global stuID
		stuID = request.form.get('stuID')
		_password = request.form.get('password')
		loginResult = Student.query.filter(and_(Student.stuID == stuID,Student._password == _password)).first()	
		if loginResult:
			if loginResult.confidency == 0:
				return render_template('studentLogin.html', error_msg = 'You are in the blacklist now. If you have any problem, please contact with the admin.')
			else:
				return redirect(url_for('Student.homepage'))
		else:
			return render_template('studentLogin.html', error_msg = 'The student ID or the password must be wrong, please try again.')

@studentBP.route('/homepagefloor1', methods=['GET','POST'])
def homepage():
	if request.method == 'GET':
		# student info
		student = Student.query.filter(Student.stuID == stuID).first()
		name = student.name

		seatInfo = Seat.query.filter(Seat.floor == 1).all()
		seatList = []
		for eachSeat in seatInfo:
			individualSeat = []
			individualSeat.append(eachSeat.sID)
			individualSeat.append(eachSeat.status)
			seatList.append(individualSeat)
		return render_template('homepagefloor1.html', seatInfo = seatList, name = name)

@studentBP.route('/homepagefloor2', methods=['GET','POST'])
def homepage2():
	if request.method == 'GET':
		# student info
		student = Student.query.filter(Student.stuID == stuID).first()
		name = student.name

		# seat Info
		seatInfo = Seat.query.filter(Seat.floor == 2).all()
		seatList = []
		for eachSeat in seatInfo:
			individualSeat = []
			individualSeat.append(eachSeat.sID)
			individualSeat.append(eachSeat.status)
			seatList.append(individualSeat)
		return render_template('homepagefloor2.html', seatInfo = seatList, name = name)

@studentBP.route('/homepagefloor3', methods=['GET','POST'])
def homepage3():
	if request.method == 'GET':
		# student info
		student = Student.query.filter(Student.stuID == stuID).first()
		name = student.name

		seatInfo = Seat.query.filter(Seat.floor == 3).all()
		seatList = []
		for eachSeat in seatInfo:
			individualSeat = []
			individualSeat.append(eachSeat.sID)
			individualSeat.append(eachSeat.status)
			seatList.append(individualSeat)
		return render_template('homepagefloor3.html', seatInfo = seatList, name = name)

@studentBP.route('/orderPage/<sID>/',methods=['GET','POST'])
def seatOrder1(sID):
	if request.method == 'GET':
		# student info
		student = Student.query.filter(Student.stuID == stuID).first()
		name = student.name

		seat = Seat.query.filter(Seat.sID == sID).first()
		floorNum = seat.floor
		return render_template('orderPage.html', sID = sID, floorNum = floorNum, visable = 1, name = name)
	else:
		# student info
		student = Student.query.filter(Student.stuID == stuID).first()
		name = student.name
		ordertmp = Order.query.filter(and_(Order.stuID == stuID, Order.status != 2)).first()
		if ordertmp:
			return render_template('orderPage.html', message = "You have booked a seat already, please check your order record.", visable = 0, name = name)
		else:
			with db.auto_commit():
				seat = Seat.query.filter(Seat.sID == sID).first()
				seat.status = 1 # booked

				order = Order()
				order.stuID = stuID
				order.sID = sID
				order.time = time.localtime()
				order.status = 0 # uncomplished
				db.session.add(order)


			return render_template('orderPage.html', message = "The seat has been already booked successfully.", visable = 0, name = name)

@studentBP.route('/bookingRecord',methods=['GET','POST'])
def bookingRecord():
	if request.method == 'GET':
		# student info
		student = Student.query.filter(Student.stuID == stuID).first()
		name = student.name

		order = Order.query.filter(Order.stuID == stuID).all()

		orderTotalList = []
		for each in order:
			orderList = []
			orderList.append(each.sID)
			sID = each.sID
			seat = Seat.query.filter(Seat.sID == sID).first()
			orderList.append(seat.floor)
			orderList.append(each.time)
			
			orderList.append(each.status)
			orderTotalList.append(orderList)

		return render_template('bookRecord.html', orderTotalList = orderTotalList, name = name)
	else:
		# student info
		student = Student.query.filter(Student.stuID == stuID).first()
		name = student.name

		with db.auto_commit():
			order = Order.query.filter(Order.stuID == stuID, Order.status == 0).first()
			sID = order.sID
			db.session.delete(order)

			seat = Seat.query.filter(Seat.sID == sID).first()
			seat.status = 0 # released

		order = Order.query.filter(Order.stuID == stuID).all()
		orderTotalList = []
		for each in order:
			orderList = []
			orderList.append(each.sID)

			sID = each.sID
			seat = Seat.query.filter(Seat.sID == sID).first()
			orderList.append(seat.floor)
			orderList.append(each.time)
			
			orderList.append(each.status)
			orderTotalList.append(orderList)


		return render_template('bookRecord.html', orderTotalList = orderTotalList, name = name)

@studentBP.route('/scanQRcode',methods=['GET'])
def scanQRcode():
	if request.method == 'GET':
		found = set()
		capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
		while capture.isOpened():
		    ret, frame = capture.read()
		    test = pyzbar.decode(frame)
		    for tests in test:
		        testdate = tests.data.decode('utf-8')
		        testtype = tests.type

		        printout = "{} ({})".format(testdate, testtype)

		        if testdate not in found:
		            print("[INFO] Found {} barcode: {}".format(testtype, testdate))
		            print(printout)
		        sID = testdate
		    cv2.imshow('Scanning', frame)
		    if cv2.waitKey(1) == ord('q'):
		        break
		capture.release()
		cv2.destroyAllWindows()
		with db.auto_commit():
			order = Order.query.filter(Order.stuID == stuID, Order.sID == sID).first()
			order.status = 1
		# student info
		student = Student.query.filter(Student.stuID == stuID).first()
		name = student.name

		return render_template('scan.html', message = "Check in successfully. :)", name = name)

@studentBP.route('/leaveSeat/<sID>/',methods=['GET'])
def leaveSeat(sID):
	if request.method == 'GET':
		with db.auto_commit():
			seat = Seat.query.filter(Seat.sID == sID).first()
			seat.status = 0
			order = Order.query.filter(Order.stuID == stuID, Order.sID == sID).first()
			order.status = 2
		# student info
		student = Student.query.filter(Student.stuID == stuID).first()
		name = student.name

		order = Order.query.filter(Order.stuID == stuID).all()

		orderTotalList = []
		for each in order:
			orderList = []
			orderList.append(each.sID)
			sID = each.sID
			seat = Seat.query.filter(Seat.sID == sID).first()
			orderList.append(seat.floor)
			orderList.append(each.time)
			
			orderList.append(each.status)
			orderTotalList.append(orderList)
		return render_template('bookRecord.html', orderTotalList = orderTotalList, name = name)

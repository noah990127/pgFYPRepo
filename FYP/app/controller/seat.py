from flask import Blueprint,render_template, request, redirect, url_for
from app.models.base import db
from app.models.student import Student
from app.models.seat import Seat
from sqlalchemy import or_,and_,all_,any_
import qrcode as qr

seatBP = Blueprint('Seat',__name__)


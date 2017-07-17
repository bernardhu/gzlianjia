# -*- coding: utf-8 -*-

from peewee import SqliteDatabase, Model, CharField, DateTimeField, IntegerField, FloatField

db = SqliteDatabase('./houseprice.db')

class TradedHouse(Model):
	xiaoqu = CharField()
	houseType = CharField()
	square = FloatField()
	houseUrl = CharField()
	orientation = CharField()
	decoration = CharField()
	elevator = CharField()
	floorLevel = CharField()
	floorTotal = IntegerField()
	build = IntegerField()
	price = IntegerField()
	tradeDate = DateTimeField()
	bid = IntegerField()
	deal = IntegerField()
	cycle = IntegerField()
	district = CharField()
	bizcircle = CharField()

	class Meta:
		database = db
                db_table = 'tradedhouse'

class BidHouse(Model):
	xiaoqu = CharField()
	houseType = CharField()
	square = FloatField()
	houseUrl = CharField()
	orientation = CharField()
	decoration = CharField()
	elevator = CharField()
	floorLevel = CharField()
	floorTotal = IntegerField()
	build = IntegerField()
	price = IntegerField()
	avg = IntegerField()
	bid = FloatField()
	watch = IntegerField()
	release = IntegerField()
	seen = IntegerField()
        district = CharField()
	bizcircle = CharField()

	class Meta:
		database = db
                db_table = 'bidhouse'

class DistricHouse(Model):
	name = CharField()
	district = CharField()
	bizcircle = CharField()
	historyRange = IntegerField()
	historySell = IntegerField()
	ref = CharField()
	avgpx = IntegerField()
	onsell = IntegerField()

	class Meta:
		database = db
                db_table = 'districhouse'

class RentHouse(Model):
	xiaoqu = CharField()
	houseType = CharField()
	square = FloatField()
	houseUrl = CharField()
	orientation = CharField()
	floorLevel = CharField()
	floorTotal = IntegerField()
	price = IntegerField()
	avg = IntegerField()
	loan = IntegerField()
	loanRet = IntegerField()
	seen = IntegerField()
        district = CharField()
	bizcircle = CharField()

	class Meta:
		database = db
                db_table = 'renthouse'

def create_table():
	db.create_tables([TradedHouse, DistricHouse, BidHouse, RentHouse])
	#db.create_tables([TradedHouse, BidHouse, RentHouse])

def clear_table():
	db.drop_tables([BidHouse, RentHouse])
	db.create_tables([BidHouse, RentHouse])

#create_table()

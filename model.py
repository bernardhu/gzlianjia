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

def create_table():
	db.create_tables([TradedHouse, DistricHouse])

#create_table()
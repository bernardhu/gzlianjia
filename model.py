# -*- coding: utf-8 -*-

from peewee import SqliteDatabase, Model, CharField, DateTimeField

db = SqliteDatabase('./houseprice.db')

class TradedHouse(Model):
	xiaoqu = CharField()
	houseType = CharField()
	square = CharField()
	houseUrl = CharField()
	orientation = CharField()
	decoration = CharField()
	elevator = CharField()
	floor = CharField()
	build = CharField()
	price = CharField()
	tradeDate = DateTimeField()
	bid = CharField()
	cycle = CharField()

	class Meta:
		database = db

class DistricHouse(Model):
	name = CharField()
	district = CharField()
	bizcircle = CharField()
	history = CharField()
	ref = CharField()
	avgpx = CharField()
	onsell = CharField()

	class Meta:
		database = db

def create_table():
	db.create_tables([TradedHouse, DistricHouse])

#create_table()

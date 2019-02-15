#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# https://api.warframestat.us/pc/voidTrader
#

class Baro:
	def __init__(self, id=None, activation=None, startString=None, expiry=None, active=None, character=None,
				location=None, inventory=None, psId=None, endString=None):
		self.id = id
		self.activation = activation
		self.startString = startString
		self.expiry = expiry
		self.active = active
		self.character = character

		node_parts = location.replace(')', '').split(' (')
		self.location = node_parts[0]
		self.planet = node_parts[1]
		self.inventory = inventory
		self.psId = psId
		self.endString = endString

	def get_baro(self):
		where = 'came' if self.active else 'is going'
		eta = '' if self.active else '. ETA: ' + self.startString
		return f"Baro Ki\'Teer {where} to {self.location}({self.planet}){eta}"


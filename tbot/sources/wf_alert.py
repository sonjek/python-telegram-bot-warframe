#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# https://api.warframestat.us/pc/alerts

from datetime import datetime
from ..utils.logging import logger


class Alert:
	def __init__(self, num, id=None, activation=None, startString=None, expiry=None,
				active=None, mission=None, eta=None, rewardTypes=None, tag=None):
		self.num = num
		self.id = id
		self.activation = activation
		self.startString = startString
		self.expiry = expiry
		self.active = active
		self.mission = mission
		self.eta = eta
		self.rewardTypes = rewardTypes
		self.description = mission['description']
		self.node = mission['node']
		node_parts = self.node.replace(')', '').split(' (')
		self.location = node_parts[0]
		self.planet = node_parts[1]
		self.type = mission['type']
		self.faction = mission['faction']
		self.reward_data = mission['reward']
		self.reward = self.reward_data['asString']
		self.rewardType = ','.join(self.rewardTypes)
		self.tag = tag

	def get_alert(self, markdown=True):
		msg = ''

		if not self.active:
			logger.info(f'@@@@ skip completed {self.node}')
			return msg

		if markdown:
			pattern = '{desc}  `ETA:` _{eta}_\n`{p} ({m})` - {type}\n{rev} ({revt})\n\n'
		else:
			pattern = '{desc}  ETA: {eta}\n {p} ({m}) - {type}\n{rev} ({revt})\n\n'

		date_time_obj = datetime.strptime(self.expiry, '%Y-%m-%dT%H:%M:%S.%fZ')
		date_diff = date_time_obj - datetime.now()
		eta = str(date_diff).split('.')[0]
		logger.info(f"@@@@ str(date_diff) {str(date_diff)} -> {str(date_diff).split('.')}")

		msg = pattern.format(
			desc=self.description, type=self.type, rev=self.reward, revt=self.rewardType,
			p=self.planet, m=self.location, eta=eta)
		return self.id, msg, self.reward, self.activation

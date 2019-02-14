#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# https://api.warframestat.us/pc/invasions
#

from ..utils.loadconfig import config

drop_excludes = config["exclude_rewards"]


class Invasion:
    def __init__(self, num, id=None, activation=None, startString=None, node=None, desc=None, attackerReward=None,
                attackingFaction=None, defenderReward=None, defendingFaction=None, vsInfestation=None,
                count=None, requiredRuns=None, completion=None, completed=None, eta=None, rewardTypes=None):
        self.num = num
        self.id = id
        self.activation = activation
        self.startString = startString
        self.node = node
        node_parts = node.replace(')', '').split(' (')
        self.location = node_parts[0]
        self.planet = node_parts[1]
        self.desc = desc
        self.attackerReward = attackerReward
        self.attackerRewardName = attackerReward['asString']
        self.attackingFaction = attackingFaction
        self.defenderReward = defenderReward
        self.defenderRewardName = defenderReward['asString']
        self.defendingFaction = defendingFaction
        self.vsInfestation = vsInfestation
        self.count = count
        self.requiredRuns = requiredRuns
        self.completion = round(completion, 1)
        self.completed = completed
        self.eta = 'No Data' if 'Infinityd' in eta else eta
        self.rewardTypes = rewardTypes

    def get_invasion(self, return_all=True, is_job=False, markdown=True):
        msg = ''

        if self.completed:
            return self.id, False, msg, '', '', '', False

        eta_info = ''
        if not is_job and markdown:
            eta_info = ', `ETA:` _{eta}_'
        elif not is_job and not markdown:
            eta_info = ', ETA: {eta}'

        if markdown:
            pattern = '`{a}` {al} ⚔️ `{d}` {dl}\n{p} ({m}), `status:` *{perc}%* ({co}/{go})' + eta_info + '\n\n'
        else:
            pattern = '{a} {al} >>> {d} {dl}\n{p} ({m}), status: {perc}% ({co}/{go})' + eta_info + '\n\n'

        a_reward = '' if self.attackerRewardName == '' else '(' + self.attackerRewardName + ')'
        d_reward = '' if self.defenderRewardName == '' else '(' + self.defenderRewardName + ')'

        rare_reward = True
        if (a_reward == '' or any(ext in a_reward for ext in drop_excludes)) and (
                d_reward == '' or any(ext in d_reward for ext in drop_excludes)):
            rare_reward = False

        if not return_all and not rare_reward:
            return self.id, rare_reward, msg, '', '', '', False

        started = abs(self.count) < self.requiredRuns
        msg = pattern.format(
                p=self.planet, m=self.location,
                a=self.attackingFaction, al=a_reward, d=self.defendingFaction, dl=d_reward,
                co=self.count, go=self.requiredRuns, t=self.startString, perc=self.completion, eta=self.eta)
        return self.id, rare_reward, msg, self.attackerRewardName, self.defenderRewardName, self.activation, started

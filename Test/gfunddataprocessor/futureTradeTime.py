# coding: utf-8
FUTURES = ['A', 'AG', 'AL', 'AU', 'B', 'BB', 'BU', 'C', 'CF', 'CS', 'CU',
           'ER', 'FB', 'FG', 'FU', 'HC', 'I', 'J', 'JD', 'JM',
           'JR', 'L', 'LR', 'M', 'MA', 'ME', 'NI', 'OI', 'P', 'PB', 'PM',
           'PP', 'RB', 'RI', 'RM', 'RO', 'RS', 'RU', 'SF', 'SM', 'SN', 'SR',
           'T', 'TA', 'TC', 'TF', 'V', 'WH', 'WR', 'WS', 'WT', 'Y', 'ZC', 'ZN',
           'IF', 'IC', 'IH']

DCE_CHANGE = '20150508'
SHFE_CHANGE = '20160503'

# 首先填充一下共同信息(当然股指期货不同，可以之后修改)
TRADETIME = {}
for future in FUTURES:
    TRADETIME[future] = {}
    TRADETIME[future]['day'] = {}
    TRADETIME[future]['day2'] = {}
    TRADETIME[future]['night'] = {}
    TRADETIME[future]['day']['open1'] = '09:00:00'
    TRADETIME[future]['day']['close1'] = '11:30:00'
    TRADETIME[future]['day']['open2'] = '13:30:00'
    TRADETIME[future]['day']['close2'] = '15:00:00'
    TRADETIME[future]['night']['open1'] = None
    TRADETIME[future]['night']['close1'] = None
    TRADETIME[future]['night']['timeChange'] = None
    TRADETIME[future]['night']['open2'] = None
    TRADETIME[future]['night']['close2'] = None

# A : 豆1
TRADETIME['A']['night']['open1'] = '21:00:00'
TRADETIME['A']['night']['close1'] = '02:30:00'
TRADETIME['A']['night']['timeChange'] = DCE_CHANGE
TRADETIME['A']['night']['open2'] = '21:00:00'
TRADETIME['A']['night']['close2'] = '23:30:00'

# A : 豆1
TRADETIME['B']['night']['open1'] = '21:00:00'
TRADETIME['B']['night']['close1'] = '02:30:00'
TRADETIME['B']['night']['timeChange'] = DCE_CHANGE
TRADETIME['B']['night']['open2'] = '21:00:00'
TRADETIME['B']['night']['close2'] = '23:30:00'

# AG : 沪银
TRADETIME['AG']['night']['open1'] = '21:00:00'
TRADETIME['AG']['night']['close1'] = '02:30:00'
TRADETIME['AG']['night']['timeChange'] = None
TRADETIME['AG']['night']['open2'] = None
TRADETIME['AG']['night']['close2'] = None

# AL : 沪铝
TRADETIME['AL']['night']['open1'] = '21:00:00'
TRADETIME['AL']['night']['close1'] = '01:00:00'
TRADETIME['AL']['night']['timeChange'] = None
TRADETIME['AL']['night']['open2'] = None
TRADETIME['AL']['night']['close2'] = None

# AU : 沪金
TRADETIME['AU']['night']['open1'] = '21:00:00'
TRADETIME['AU']['night']['close1'] = '02:30:00'
TRADETIME['AU']['night']['timeChange'] = None
TRADETIME['AU']['night']['open2'] = None
TRADETIME['AU']['night']['close2'] = None

# BB : 胶合板   无夜盘

# BU : 沥青
TRADETIME['BU']['night']['open1'] = '21:00:00'
TRADETIME['BU']['night']['close1'] = '01:00:00'
TRADETIME['BU']['night']['timeChange'] = SHFE_CHANGE
TRADETIME['BU']['night']['open2'] = '21:00:00'
TRADETIME['BU']['night']['close2'] = '23:00:00'

# C : 玉米  无夜盘

# CF : 棉花
TRADETIME['CF']['night']['open1'] = '21:00:00'
TRADETIME['CF']['night']['close1'] = '23:30:00'
TRADETIME['CF']['night']['timeChange'] = None
TRADETIME['CF']['night']['open2'] = None
TRADETIME['CF']['night']['close2'] = None

# CS : 玉米淀粉 无夜盘

# CU : 沪铜
TRADETIME['CU']['night']['open1'] = '21:00:00'
TRADETIME['CU']['night']['close1'] = '01:00:00'
TRADETIME['CU']['night']['timeChange'] = None
TRADETIME['CU']['night']['open2'] = None
TRADETIME['CU']['night']['close2'] = None

# ER : 早籼稻10吨   无夜盘

# FB : 纤维板   无夜盘

# FG : 玻璃
TRADETIME['FG']['night']['open1'] = '21:00:00'
TRADETIME['FG']['night']['close1'] = '23:00:00'
TRADETIME['FG']['night']['timeChange'] = None
TRADETIME['FG']['night']['open2'] = None
TRADETIME['FG']['night']['close2'] = None

# FU : 燃油 无夜盘

# HC : 热轧卷板
TRADETIME['HC']['night']['open1'] = '21:00:00'
TRADETIME['HC']['night']['close1'] = '01:00:00'
TRADETIME['HC']['night']['timeChange'] = SHFE_CHANGE
TRADETIME['HC']['night']['open2'] = '21:00:00'
TRADETIME['HC']['night']['close2'] = '23:00:00'

# I : 铁矿石
TRADETIME['I']['night']['open1'] = '21:00:00'
TRADETIME['I']['night']['close1'] = '02:30:00'
TRADETIME['I']['night']['timeChange'] = DCE_CHANGE
TRADETIME['I']['night']['open2'] = '21:00:00'
TRADETIME['I']['night']['close2'] = '23:30:00'


# J : 焦炭
TRADETIME['J']['night']['open1'] = '21:00:00'
TRADETIME['J']['night']['close1'] = '02:30:00'
TRADETIME['J']['night']['timeChange'] = DCE_CHANGE
TRADETIME['J']['night']['open2'] = '21:00:00'
TRADETIME['J']['night']['close2'] = '23:30:00'

# JD : 鸡蛋 无夜盘

# JM : 焦煤
TRADETIME['JM']['night']['open1'] = '21:00:00'
TRADETIME['JM']['night']['close1'] = '02:30:00'
TRADETIME['JM']['night']['timeChange'] = DCE_CHANGE
TRADETIME['JM']['night']['open2'] = '21:00:00'
TRADETIME['JM']['night']['close2'] = '23:30:00'

# JR : 粳稻 无夜盘

# L : 塑料 无夜盘

# LR ：晚籼稻   无夜盘

# M : 豆粕
TRADETIME['M']['night']['open1'] = '21:00:00'
TRADETIME['M']['night']['close1'] = '02:30:00'
TRADETIME['M']['night']['timeChange'] = DCE_CHANGE
TRADETIME['M']['night']['open2'] = '21:00:00'
TRADETIME['M']['night']['close2'] = '23:30:00'

# MA : 甲醇10吨
TRADETIME['MA']['night']['open1'] = '21:00:00'
TRADETIME['MA']['night']['close1'] = '23:00:00'
TRADETIME['MA']['night']['timeChange'] = None
TRADETIME['MA']['night']['open2'] = None
TRADETIME['MA']['night']['close2'] = None

# ME : 甲醇50吨
TRADETIME['ME']['night']['open1'] = '21:00:00'
TRADETIME['ME']['night']['close1'] = '23:00:00'
TRADETIME['ME']['night']['timeChange'] = None
TRADETIME['ME']['night']['open2'] = None
TRADETIME['ME']['night']['close2'] = None

# NI : 镍
TRADETIME['NI']['night']['open1'] = '21:00:00'
TRADETIME['NI']['night']['close1'] = '01:00:00'
TRADETIME['NI']['night']['timeChange'] = None
TRADETIME['NI']['night']['open2'] = None
TRADETIME['NI']['night']['close2'] = None

# OI : 菜油10吨
TRADETIME['OI']['night']['open1'] = '21:00:00'
TRADETIME['OI']['night']['close1'] = '23:00:00'
TRADETIME['OI']['night']['timeChange'] = None
TRADETIME['OI']['night']['open2'] = None
TRADETIME['OI']['night']['close2'] = None

# P : 棕榈油
TRADETIME['P']['night']['open1'] = '21:00:00'
TRADETIME['P']['night']['close1'] = '02:30:00'
TRADETIME['P']['night']['timeChange'] = DCE_CHANGE
TRADETIME['P']['night']['open2'] = '21:00:00'
TRADETIME['P']['night']['close2'] = '23:30:00'

# PB : 铅
TRADETIME['PB']['night']['open1'] = '21:00:00'
TRADETIME['PB']['night']['close1'] = '01:00:00'
TRADETIME['PB']['night']['timeChange'] = None
TRADETIME['PB']['night']['open2'] = None
TRADETIME['PB']['night']['close2'] = None

# PM : 普麦  无夜盘

# PP : 聚丙烯   无夜盘

# RB : 螺纹钢
TRADETIME['RB']['night']['open1'] = '21:00:00'
TRADETIME['RB']['night']['close1'] = '01:00:00'
TRADETIME['RB']['night']['timeChange'] = SHFE_CHANGE
TRADETIME['RB']['night']['open2'] = '21:00:00'
TRADETIME['RB']['night']['close2'] = '23:00:00'

# RI : 早籼稻200英担    无夜盘

# RM : 菜粕
TRADETIME['RM']['night']['open1'] = '21:00:00'
TRADETIME['RM']['night']['close1'] = '23:00:00'
TRADETIME['RM']['night']['timeChange'] = None
TRADETIME['RM']['night']['open2'] = None
TRADETIME['RM']['night']['close2'] = None

# RO : 菜油5吨  无夜盘

# RS : 菜籽 无夜盘

# RU : 橡胶
TRADETIME['RU']['night']['open1'] = '21:00:00'
TRADETIME['RU']['night']['close1'] = '23:00:00'
TRADETIME['RU']['night']['timeChange'] = None
TRADETIME['RU']['night']['open2'] = None
TRADETIME['RU']['night']['close2'] = None

# SF : 硅铁 无夜盘

# SM : 锰硅 无夜盘

# SN : 沪锡
TRADETIME['SN']['night']['open1'] = '21:00:00'
TRADETIME['SN']['night']['close1'] = '01:00:00'
TRADETIME['SN']['night']['timeChange'] = None
TRADETIME['SN']['night']['open2'] = None
TRADETIME['SN']['night']['close2'] = None

# SR : 白糖
TRADETIME['SR']['night']['open1'] = '21:00:00'
TRADETIME['SR']['night']['close1'] = '23:30:00'
TRADETIME['SR']['night']['timeChange'] = None
TRADETIME['SR']['night']['open2'] = None
TRADETIME['SR']['night']['close2'] = None

# T : 10年期国债    无夜盘
TRADETIME['T']['day']['open1'] = '09:15:00'
TRADETIME['T']['day']['close1'] = '11:30:00'
TRADETIME['T']['day']['open2'] = '13:30:00'
TRADETIME['T']['day']['close2'] = '15:15:00'

# TA : PTA
TRADETIME['TA']['night']['open1'] = '21:00:00'
TRADETIME['TA']['night']['close1'] = '23:30:00'
TRADETIME['TA']['night']['timeChange'] = None
TRADETIME['TA']['night']['open2'] = None
TRADETIME['TA']['night']['close2'] = None

# TC : 动力煤200吨
TRADETIME['TC']['night']['open1'] = '21:00:00'
TRADETIME['TC']['night']['close1'] = '23:30:00'
TRADETIME['TC']['night']['timeChange'] = None
TRADETIME['TC']['night']['open2'] = None
TRADETIME['TC']['night']['close2'] = None

# TF : 5年期国债
TRADETIME['TF']['day']['open1'] = '09:15:00'
TRADETIME['TF']['day']['close1'] = '11:30:00'
TRADETIME['TF']['day']['open2'] = '13:30:00'
TRADETIME['TF']['day']['close2'] = '15:15:00'

# V : PVC   无夜盘

# WH : 强麦5000蒲式耳   无夜盘

# WR : 线材 无夜盘

# WS : 强麦10吨 无夜盘

# WT : 硬麦 无夜盘

# Y : 豆油
TRADETIME['Y']['night']['open1'] = '21:00:00'
TRADETIME['Y']['night']['close1'] = '02:30:00'
TRADETIME['Y']['night']['timeChange'] = DCE_CHANGE
TRADETIME['Y']['night']['open2'] = '21:00:00'
TRADETIME['Y']['night']['close2'] = '23:30:00'

# ZC : 动力煤100吨
TRADETIME['ZC']['night']['open1'] = '21:00:00'
TRADETIME['ZC']['night']['close1'] = '23:30:00'
TRADETIME['ZC']['night']['timeChange'] = None
TRADETIME['ZC']['night']['open2'] = None
TRADETIME['ZC']['night']['close2'] = None

# ZN : 沪锌
TRADETIME['ZN']['night']['open1'] = '21:00:00'
TRADETIME['ZN']['night']['close1'] = '01:00:00'
TRADETIME['ZN']['night']['timeChange'] = None
TRADETIME['ZN']['night']['open2'] = None
TRADETIME['ZN']['night']['close2'] = None

# IC : ...
TRADETIME['IC']['day']['open1'] = '09:15:00'
TRADETIME['IC']['day']['close1'] = '11:30:00'
TRADETIME['IC']['day']['open2'] = '13:00:00'
TRADETIME['IC']['day']['close2'] = '15:15:00'
TRADETIME['IC']['day']['dayChange'] = '20160104'
TRADETIME['IC']['day2']['open1'] = '09:30:00'
TRADETIME['IC']['day2']['close1'] = '11:30:00'
TRADETIME['IC']['day2']['open2'] = '13:00:00'
TRADETIME['IC']['day2']['close2'] = '15:00:00'

# IF : ...
TRADETIME['IF']['day']['open1'] = '09:15:00'
TRADETIME['IF']['day']['close1'] = '11:30:00'
TRADETIME['IF']['day']['open2'] = '13:00:00'
TRADETIME['IF']['day']['close2'] = '15:15:00'
TRADETIME['IF']['day']['dayChange'] = '20160104'
TRADETIME['IF']['day2']['open1'] = '09:30:00'
TRADETIME['IF']['day2']['close1'] = '11:30:00'
TRADETIME['IF']['day2']['open2'] = '13:00:00'
TRADETIME['IF']['day2']['close2'] = '15:00:00'

# IH : ...
TRADETIME['IH']['day']['open1'] = '09:15:00'
TRADETIME['IH']['day']['close1'] = '11:30:00'
TRADETIME['IH']['day']['open2'] = '13:00:00'
TRADETIME['IH']['day']['close2'] = '15:15:00'
TRADETIME['IH']['day']['dayChange'] = '20160104'
TRADETIME['IH']['day2']['open1'] = '09:30:00'
TRADETIME['IH']['day2']['close1'] = '11:30:00'
TRADETIME['IH']['day2']['open2'] = '13:00:00'
TRADETIME['IH']['day2']['close2'] = '15:00:00'

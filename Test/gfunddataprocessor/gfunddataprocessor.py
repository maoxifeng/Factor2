# coding: utf-8

from __future__ import division

import datetime as dtime
import os
import re
import gzip
import time
import multiprocessing as mp

import numpy as np
import pandas as pd
import tick_pb2 as tp

from globallogger import logger
from cStringIO import StringIO
from futureTradeTime import TRADETIME
from futureTradeTime import FUTURES
from mongo import MongoDB

################################################################
#   mongodb are choosed as the defualt database
#   maybe we should write a wrapper to seperate
#   the database query operation
#   this module maybe helpful later:
#   sqltomongo: https://github.com/klausdk/sqltomongodb
#   but that's a tedious work, do it later
################################################################
# mdb = MongoDB()
# db = mdb.client['futures']
# coll_zhongxin = db['future2']
# coll_yinhe = db['future_yinhe4']

################################################################
# the return of all "get_..." function has a common format:
# DataFrame of Pandas
################################################################

ZHONGXIN = 0
YINHE = 1
SZ = 'SZ'
SH = 'SH'

STOCK_TICK_PATH = '/data/tdb/tick.pb.gz'
MARKET = {'1011': 'sh', '1012': 'sz'}

DAY_TYPE = 0
NIGHT_TYPE = 1

COLUMNS = [e.name for e in tp.Tick.DESCRIPTOR.fields]
COLUMNS.append('instrument_id')
COLUMNS.append('type')
PRICE_LIST = [
    'price', 'turnover', 'acc_turnover', 'high', 'low', 'open', 'pre_close',
    'pre_close', 'settle', 'pre_settle', 'cur_delta',
    'ask_price1', 'ask_price2', 'ask_price3', 'ask_price4', 'ask_price5',
    'ask_price6', 'ask_price7', 'ask_price8', 'ask_price9', 'ask_price10',
    'bid_price1', 'bid_price2', 'bid_price3', 'bid_price4', 'bid_price5',
    'bid_price6', 'bid_price7', 'bid_price8', 'bid_price9', 'bid_price10',
    'ask_avg_price', 'bid_avg_price', 'index']
PRICE_ORDER = [COLUMNS.index(e) for e in PRICE_LIST]
ALL_COLUMNS = COLUMNS
COLUMNS_SET = set(COLUMNS)
DEFAULT_COLUMNS = ['instrument_id', 'price', 'bid_price1', 'bid_volume1',
                   'ask_price1', 'ask_volume1', 'interest', 'volume']

NIGHT = 0
MORNING = 1
AFTERNOON = 2
ALL_PERIOD = [NIGHT, MORNING, AFTERNOON]

process_num = 8


def set_process_num(n):
    global process_num
    process_num = n


def _is_futures(symbol):
    symbol = symbol.upper()
    pat_future = re.compile(r'^([A-Z]+)(\d+){0,1}$')
    ID_parts = pat_future.search(symbol)

    if ID_parts:
        return True
    else:
        pat_stock = re.compile(r'^(\d+)\.([A-Z]{2})$')
        ID_parts = pat_stock.search(symbol)
        assert ID_parts is not None
        return False


def _get_current_coll(data_source):
    mdb = MongoDB()
    db = mdb.client['futures']
    if data_source == ZHONGXIN:
        coll_now = db['future2']
    elif data_source == YINHE:
        coll_now = db['future_yinhe4']
    else:
        coll_now = None
    return coll_now


def get_main_contract(fuid, days, columns=DEFAULT_COLUMNS, merge=True,
                      data_source=YINHE, pad=False, indayperiod=ALL_PERIOD,
                      indaymerge=True):
    if merge:
        assert indaymerge, "inday_merge should be True when merge is True"

    if type(days) == int or type(days) == str:
        days = [days]

    if type(days) != tuple and type(days) != list:
        logger.error('parameter error!!')
        return None

    if type(days) == tuple and len(days) != 2:
        logger.error('parameter error!!')
        return None

    mdb1 = MongoDB()
    db1 = mdb1.client['futures']
    coll1 = db1['main_contracts']
    coll_now = _get_current_coll(data_source)

    if type(days) == list:
        cursor = coll1.find(
            {
                'TradingDay': {'$in': [int(e) for e in days]},
                'InstrumentID': {'$regex': re.compile('^'+fuid+r'\d+$')}})
    else:
        cursor = coll1.find(
            {
                'TradingDay': {'$gte': int(days[0]), '$lte': int(days[1])},
                'InstrumentID': {'$regex': re.compile('^'+fuid+r'\d+$')}})
    df_main = pd.DataFrame(list(cursor))
    if df_main.empty:
        logger.warn('found nothing, maybe not trading days')
        return None
    pairs = zip(df_main.TradingDay, df_main.InstrumentID)

    if df_main.empty:
        return None

    # 一次取出冗余的数据后进行筛选， 减少query次数
    cursor = coll_now.find(
        {
            'TradingDay': {'$in': df_main.TradingDay.tolist()},
            'InstrumentID': {'$in': list(set(df_main.InstrumentID.tolist()))}})
    df_tmp = pd.DataFrame(list(cursor))
    df_res = df_tmp[[(
        df_tmp.loc[i]['TradingDay'], df_tmp.loc[i]['InstrumentID'])
        in pairs for i in range(len(df_tmp.index))]]

    if len(df_res) == 0:
        return None
    elif len(df_res) < 5:
        res = _decode_tick_data(df_res, columns, pad, indayperiod, indaymerge)
    else:
        pool = mp.Pool(processes=process_num)
        res = []
        for df in _chunks(df_res, 1):
            res.append(pool.apply_async(_decode_tick_data, (df, columns, pad,
                       indayperiod, indaymerge)))
        pool.close()
        pool.join()

        res = map(lambda ret: ret.get(), res)
        # flatten the list.
        res = [item for sublist in res for item in sublist]

    if merge:
        res = pd.concat(res)

    return res

##############################################################
# 这里先只考虑期货， 股票数据录入了再重构， 一步一步来
##############################################################


def _get_stock_from_files(symbol, days, market_id=None):
    # 20121101 20121102
    alldays = os.listdir(STOCK_TICK_PATH)
    alldays.sort()
    if type(days) == list:
        targets = [str(e) for e in days if str(e) in alldays]
    elif type(days) == tuple:
        targets = [e for e in alldays if e >= str(days[0])
                   and e <= str(days[1])]
    else:
        logger.error('invalid type of parameter days')
        return None
    reslist = []
    for day in targets:
        sdict = {}
        day_path = os.path.join(STOCK_TICK_PATH, day)
        # 1101, 1102
        if market_id not in [SZ, SH]:
            logger.error("invalid market "+str(market_id))
            return None
        elif market_id == SZ:
            market = '1012'
        elif market_id == SH:
            market = '1011'

        market_path = os.path.join(day_path, market)
        name = symbol+'.pb.gz'
        # 124081.pb.gz, 124895.pb.gz
        if name not in os.listdir(market_path):
            continue
        sdict['InstrumentID'] = symbol+'.'+MARKET[market]
        sdict['Type'] = 0
        sdict['content'] = open(os.path.join(market_path, name),
                                'rb').read()
        sdict['TradingDay'] = int(day)
        reslist.append(sdict)
    return pd.DataFrame(reslist)


def get_stock_factor(symbol, date=None, columns=['symbol', 'date',
                                                 'adjustingfactor',
                                                 'adjustconst',
                                                 'radioadjustfactor']):
    mdb = MongoDB()
    db = mdb.client['futures']
    coll_factor = db['stockfactor']
    if date is None:
        cursor = coll_factor.find({'symbol': symbol},
                                  projection=columns)
    elif type(date) == tuple:
        cursor = coll_factor.find({'symbol': symbol,
                                   'date': {'$gte': int(date[0]),
                                            '$lte': int(date[1])}},
                                  projection=columns)
    else:
        cursor = coll_factor.find({'symbol': symbol, 'date': int(date)},
                                  projection=columns)
    cursor = list(cursor)
    if not cursor:
        return None
    else:
        res = pd.DataFrame(cursor)
        del res['_id']
        return res


def get_day_tick(symbol, days, columns=DEFAULT_COLUMNS, merge=True,
                 data_source=YINHE, pad=False, indayperiod=ALL_PERIOD,
                 indaymerge=True):
    if merge:
        assert indaymerge, "inday_merge should be True when merge is True"

    indayperiod.sort()

    def judge_period(period=indayperiod):
        tmp = np.array(period)
        if tmp.max() > AFTERNOON or np.bincount(tmp).max() > 1:
            return False
        # 取夜盘和下午盘
        if tmp.size == 2 and tmp[0] == 0 and tmp[1] == 2:
            return False
        return True

    if not judge_period(indayperiod):
        raise ValueError("Invalid inday period parameter")

    # 判断是股票还是期货
    flag = 'FUTURE'
    symbol = symbol.upper()
    pat_future = re.compile(r'^([A-Z]+)(\d+){0,1}$')
    pat_stock = re.compile(r'^(\d+)\.([A-Z]{2})$')
    ID_parts = pat_future.search(symbol)
    security_ID = fdate = None
    if ID_parts:
        security_ID, fdate = ID_parts.groups()
    else:
        ID_parts = pat_stock.search(symbol)
        if ID_parts is None:
            logger.error('invalid symbol '+symbol)
            return None
        security_ID, market = ID_parts.groups()
        flag = 'STOCK'

    # 查询期货代码是否在数据库中
    if security_ID not in FUTURES and flag == 'FUTURE':
        logger.error(security_ID + ' not found in futures base')
        return None

    if type(days) == int or type(days) == str:
        days = [days]

    if type(days) != tuple and type(days) != list:
        logger.error('parameter type error!!')
        return None

    if type(days) == tuple and len(days) != 2:
        logger.error('parameter type error!!')
        return None

    if not all([isinstance(e, type(days[0])) for e in days]):
        logger.error('parameter type error!!')
        return None

    coll_now = _get_current_coll(data_source)

    if not fdate and flag == 'FUTURE':
        # extract specific period in one day
        return get_main_contract(security_ID, days, columns,
                                 merge, data_source, pad, indayperiod,
                                 indaymerge)

    # 从mongodb中获取期货数据
    if flag == 'FUTURE':
        if hasattr(days[0], 'strftime'):
            days = [e.strftime('%Y%m%d') for e in days]
        if type(days) == list:
            cursor = coll_now.find({
                'TradingDay': {'$in': [int(i) for i in days]},
                'InstrumentID': symbol})

        if type(days) == tuple:
            cursor = coll_now.find({
                'TradingDay': {'$gte': int(days[0]), '$lte': int(days[1])},
                'InstrumentID': symbol})

        df_res = pd.DataFrame(list(cursor))
    # 从文件系统中获取股票数据
    else:
        df_res = _get_stock_from_files(security_ID, days, market)

    if len(df_res) == 0:
        return None
    elif len(df_res) < 5:
        res = _decode_tick_data(df_res, columns, pad, indayperiod, indaymerge)
        res = [item.drop([pd.NaT]) if pd.NaT in item.index else item for item in res]

        # 去掉非法的时间(比如09:25之前)
        res = [item.drop(
               item.index[item.index <
                          (item.index[0].strftime("%Y-%m-%d")+" 09:25:00")])
               for item in res
               if item is not None]
        res = [item.drop(item.index[item.price < 0.01]) for item in res]
    else:
        pool = mp.Pool(processes=process_num)
        res = []
        for df in _chunks(df_res, 1):
            res.append(pool.apply_async(_decode_tick_data, (df, columns, pad,
                       indayperiod, indaymerge)))
        pool.close()
        pool.join()

        res = map(lambda ret: ret.get(), res)
        # flatten the list.
        res = [item.drop([pd.NaT]) if pd.NaT in item.index else item for sublist in res for item in sublist]

        # 去掉非法的时间(比如09:25之前)
        res = [item.drop(
               item.index[item.index <
                          (item.index[0].strftime("%Y-%m-%d")+" 09:25:00")])
               for item in res
               if item is not None]
        res = [item.drop(item.index[item.price < 0.01]) for item in res]

    if merge:
        if len(res) > 0:
            res = pd.concat(res)

    return res


def get_filled_tick_data(symbol, start, end=None):
    pass


def get_bar_data():
    pass


# TODO(reed): This method is unstable(since the structure of `TRADETIME` is not
# reasonable), it may need modification.
def _get_rest_time(symbol, day, time_type=None):
    pat_future = re.compile(r'^([A-Z]+)(\d+){0,1}$')
    pat_stock = re.compile(r'^(\d+)\.([A-Z]{2})$')
    ID_parts = pat_future.search(symbol)
    security_ID = fdate = None
    if ID_parts:
        security_ID, fdate = ID_parts.groups()
        flag = 'FUTURE'
    else:
        ID_parts = pat_stock.search(symbol)
        assert ID_parts is not None
        security_ID, market = ID_parts.groups()
        flag = 'STOCK'

    if flag == 'FUTURE':
        # FIXME(reed): Commodity futures rests at [10:15, 10:30].
        daystart1 = TRADETIME[security_ID]['day']['open1']
        dayend1 = TRADETIME[security_ID]['day']['close1']
        daystart2 = TRADETIME[security_ID]['day']['open2']
        # end2 = TRADETIME[security_ID]['day']['close2']
        # 如果是股指期货， 中间日盘时间进行过调整， 需要判断
        trading_day = day.year * 10000 + day.month * 100 + day.day
        if 'dayChange' in TRADETIME[security_ID]['day']:
            day_change = int(TRADETIME[security_ID]['day']['dayChange'])
            if trading_day >= day_change:
                daystart1 = TRADETIME[security_ID]['day2']['open1']
                dayend1 = TRADETIME[security_ID]['day2']['close1']
                daystart2 = TRADETIME[security_ID]['day2']['open2']
                # end2 = TRADETIME[security_ID]['day2']['close2']
        nightend = None
        if TRADETIME[security_ID]['night']['close1']:
            nightend = TRADETIME[security_ID]['night']['close1']
            timechange = TRADETIME[security_ID]['night']['timeChange']
            if timechange and trading_day >= int(timechange):
                nightend = TRADETIME[security_ID]['night']['close2']

        yestoday = (pd.Timestamp(day) + dtime.timedelta(days=-1))
        # 此处需要区分夜盘是当天结束(24:00之前)还是第二天结束
        # 1. 有夜盘且在24点之前结束
        if nightend and nightend > '19:00:00':
            return [(yestoday + pd.to_timedelta(nightend),
                    day + pd.to_timedelta(daystart1)),
                    (day + pd.to_timedelta(dayend1),
                    day + pd.to_timedelta(daystart2))]
        # 2. 有夜盘且在24点之后结束
        elif nightend:
            return [(day + pd.to_timedelta(nightend),
                    day + pd.to_timedelta(daystart1)),
                    (day + pd.to_timedelta(dayend1),
                    day + pd.to_timedelta(daystart2))]
        # 3. 该品种没有夜盘
        else:
            return [(day + pd.to_timedelta(dayend1),
                    day + pd.to_timedelta(daystart2))]
    else:
        return [(day, day + pd.to_timedelta('9:30:00')),
                (day + pd.to_timedelta('11:30:00'),
                 day + pd.to_timedelta('13:00:00'))]


def _tick2bar(symbol, tick_data, freq):
    """ Transform tick data into bar data.
    """
    column_list = []
    time_type = None
    # NOTE: indaymerge为False的时候，穿入的是list
    # 为True的时候传入的是dataframe，全部转化为list后处理
    # 在最后返回时，根据标志区分
    splitflag = False
    if type(tick_data) == list:
        splitflag = True
    else:
        tick_data = [tick_data, ]
    # 由于区分了夜盘和上下午， 这里tickdata最多为3段
    for period in tick_data:
        tmp_list = []
        # 夜盘有时候没有数据
        if period.empty:
            column_list.append(tmp_list)
            continue

        for name, col in period.iteritems():
            if name in ['volume', 'turnover']:
                col_df = col.resample(freq).sum()
                # If not all elements are nan, fill nan with 0.
                if not col_df.isnull().all():
                    col_df.fillna(0, inplace=True)
            elif name == 'price':
                col_df = col.resample(freq).ohlc()
                closes = col_df['close'].fillna(method='pad')
                col_df = col_df.apply(lambda x: x.fillna(closes))
            # TODO(reed): Using last value isn't suitable for all other
            # columns, but for Futures it's enough now. CHECK IT LATER.
            else:
                col_df = col.resample(freq).last().fillna(method='pad')
                # Use to distinct day or night.
                if name == 'type':
                    time_type = col.iloc[0]

            # column_list.append(col_df)
            tmp_list.append(col_df)
        column_list.append(tmp_list)

    # Concat all columns.
    # bar_data = pd.concat(column_list, axis=1)
    bar_data_list = [pd.concat(ele, axis=1) if ele else pd.DataFrame()
                     for ele in column_list]

    # Filter data according to the trading time.
    # 0 out of index, maybe there's a day with out any data
    # 一天中可能出现 “上午没数据”、“下午没数据”、“夜盘没数据”三种情况，
    # 但不会出现全部没数据的情况， 下面first_time需要遍历获取
    # try:
    #     first_time = tick_data[-1].index[0]
    # except:
    #     if splitflag:
    #         return [pd.DataFrame()] * len(tick_data)
    #     else:
    #         return pd.DataFrame()
    first_time = None
    for data in tick_data:
        if not data.empty:
            first_time = data.index[0]
            break
    today = first_time.normalize()
    # 分开获取， 可能取到夜盘日期，需要加1
    if first_time.hour > 15:
        today = today + dtime.timedelta(days=1)
    if time_type is None:
        time_type = NIGHT_TYPE if first_time.hour > 15 else DAY_TYPE
    rest_time_list = _get_rest_time(symbol, today)
    # NOTE(reed): All columns share the same index, so we just use the last
    # col to generate index.
    # 如果日内分段，表示已经进行过了局部drop
    if not splitflag:
        for start, end in rest_time_list:
            for bar_data in bar_data_list:
                bar_data.drop(
                    bar_data.index[(bar_data.index >= start) &
                                   (bar_data.index < end)],
                    inplace=True)

    if splitflag:
        return bar_data_list
    return bar_data_list[0]


def get_day_bar(symbol, days, freq='1T', columns=DEFAULT_COLUMNS, merge=True,
                data_source=YINHE, indayperiod=ALL_PERIOD, indaymerge=True):
    """Get bar data (k-lines) of specific symbol, days and frequency etc.

    This method fetch bar data of specific days. It receives similar parameters
    with :meth:`get_day_tick` method, and has an particular parameter `freq`,
    which assign the frequency of bar data.

    In order to see how to set 'freq', please refer to:
    http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases

    Some frequently-used freq are:
        L, ms   milliseconds
        S       secondly frequency
        T, min  minutely frequency
        H       hourly frequency
        B       business day frequency
        D       calendar day frequency
        W       weekly frequency
        M       month end frequency

    Args:
        symbol(str): Symbol of securities.
        days(int, str, pair of int, pair of str, list of int or list of str):
            Date or date range for data. when it's single int or str, it means
            the specific day; when it's pair of days, like ``(day1, day2)``,
            it means date range from ``day1`` to ``day2``, with ``day1`` and
            ``day2`` including; otherwise when it's list of days, like
            ``[day1, day2, day3]``, it means discrete days ``day1``, ``day2``
            and ``day3``.
        freq(str): Time frequency for k-lines, like ``1S``, ``5T`` etc.
        columns(list of str): Data columns to get, like ``price``, ``volume``
            etc.
        merge(bool): When ``freq`` is inner-day frequency, ``merge`` controls
            whether to merge data from each days; otherwise when ``freq`` is
            beyond inner-day frequency, like day, week or month frequency,
            this parameter MAKES NO SENSE.
        data_source(str): Data source, ZHONGXIN or YINHE.

    Returns:
        DataFrame or list of DataFrame: DataFrame containing all bar data or
            list of DataFrame, each DataFrame in the list for one day.

    .. seealso::
        See :meth:`get_day_tick` for tick data.
    """

    if merge:
        assert indaymerge, "inday_merge should be True when merge is True"

    symbol = symbol.upper()
    # Get tick data first.
    # t1 = time.time()
    tick_data_list = get_day_tick(symbol, days, columns=columns, merge=False,
                                  data_source=data_source,
                                  indayperiod=indayperiod,
                                  indaymerge=indaymerge)
    # t2 = time.time()
    # print "get_day_tick spend time: ", t2-t1
    if tick_data_list is None:
        return None

    dts = pd.date_range('19700101', periods=2, freq=freq)
    delta = (dts[1] - dts[0]).total_seconds()
    # Inner-day frequency
    if delta < 86400:
        res = []
        if len(tick_data_list) < 5:
            for tick_data in tick_data_list:
                bar_data = _tick2bar(symbol, tick_data, freq)
                res.append(bar_data)
        else:
            pool = mp.Pool(processes=process_num)
            for tick_data in tick_data_list:
                res.append(pool.apply_async(_tick2bar,
                                            (symbol, tick_data, freq)))
            pool.close()
            pool.join()

            # t3 = time.time()
            # print "_tick2bar spend time: ", t3-t2

            res = map(lambda ret: ret.get(), res)

        if merge:
            res = pd.concat(res)

        return res
    # Beyond day frequency.
    else:
        # TODO(lym): 这里如果区分上下午会怎么样？ 之后分析
        tick_data = pd.concat(tick_data_list)
        res = _tick2bar(symbol, tick_data, freq)
        res.dropna(inplace=True)

    return res


def _extract_contract_time(timestr, symbol):
    pat = re.compile(
        r'(\d{8})-{0,1}((\d{2}):(\d{2}):(\d{2})|(\d{2}):(\d{2})|(\d{2})|$)')
    try:
        time_list = pat.search(timestr).groups()
    except Exception, ee:
        logger.error(str(ee))
        return None, None
    ret_date = int(time_list[0])
    if not time_list[1]:
        res_time = TRADETIME[symbol]['day']['open1']
    else:
        if time_list[2]:
            res_time = ':'.join([e.zfill(2) for e in time_list[2:5]])
        if time_list[5]:
            res_time = time_list[5].zfill(2)+':'+time_list[6].zfill(2)+':00'
        if time_list[7]:
            res_time = time_list[7].zfill(2)+':00:00'
    return ret_date, res_time


def get_data_bar():
    pass


def _chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


# this is a important function
def _decode_tick_data(infoFrame, columns, pad=False,
                      indayperiod=ALL_PERIOD, indaymerge=True):
    if infoFrame.empty:
        return None

    # Check the validation of columns.
    illegal_column_set = set(columns) - COLUMNS_SET
    if len(illegal_column_set):
        logger.error('illegal columns: %s', tuple(illegal_column_set))
        return None

    expand_columns = list(columns)

    if 'volume' in columns and 'acc_volume' not in columns:
        expand_columns.append('acc_volume')
    if 'turnover' in columns and 'acc_turnover' not in columns:
        expand_columns.append('acc_turnover')

    result = []
    base = [-1] * len(expand_columns)
    # instrument_id, TradingDay, content, type
    # 重新构建PRICE_LIST
    local_price_list = [e for e in expand_columns if e in PRICE_LIST]
    for i, element in infoFrame.iterrows():
        instrument_id = element['InstrumentID']
        time_type = element['Type']
        zipinfo = element['content']
        day_info = tp.TickList()
        buf = StringIO(zipinfo)
        with gzip.GzipFile(mode='rb', fileobj=buf) as gf:
            zipinfo = gf.read()
        day_info.ParseFromString(zipinfo)
        # TODO(lym): 长度需要裁剪
        if len(day_info.tick) == 0:
            continue
        filedata = np.empty((len(day_info.tick), len(expand_columns)),
                            dtype=np.int64)
        time_list = np.empty((len(day_info.tick),), dtype=np.int32)
        # 这里根据需要取得是 上午、下午和夜盘的数据来进行局部解析
        # 在csv的排列顺序是 夜盘， 上午， 下午
        morningbegin = None
        afternoonbegin = None
        endline = -1
        for indd, info in enumerate(day_info.tick):
            base = [getattr(info, ele) if ele not in ['instrument_id', 'type']
                    and info.HasField(ele) else base[j]
                    for j, ele in enumerate(expand_columns)]
            filedata[indd] = base
            # Maintain time list.
            time_list[indd] = (getattr(info, 'time') if info.HasField('time')
                               else time_list[indd-1])
            nowtime = int(time_list[indd])
            # 夜盘跳出条件
            if nowtime > 80000000 and nowtime < 190000000:
                if morningbegin is None:
                    morningbegin = str(time_list[indd]).zfill(9)
                    morningbegin = morningbegin[:2]+':'+morningbegin[2:4] + \
                        ':' + morningbegin[4:6]+'.'+morningbegin[6:]
                if indayperiod[-1] == NIGHT:
                    endline = indd
                    break
            # 上午盘跳出条件
            if nowtime > 120000000 and nowtime < 190000000:
                if afternoonbegin is None:
                    afternoonbegin = str(time_list[indd]).zfill(9)
                    afternoonbegin = (
                        afternoonbegin[:2]+':'+afternoonbegin[2:4] +
                        ':' + afternoonbegin[4:6]+'.'+afternoonbegin[6:])
                if indayperiod[-1] == MORNING:
                    endline = indd
                    break
            # 下午盘跳出， 即取出全天数据
        if indayperiod[-1] == AFTERNOON:
            endline = len(day_info.tick)

        filedata = filedata[:endline]
        time_list = time_list[:endline]

        if pad:
            # NOTE(reed): Fix wrong format time_list which affects padding,
            # like:
            #     9:00:00.000
            #     9:00:00.010
            #     9:00:01.000
            #     9:00:01.010
            #     ...
            #
            # After modification, it should be like:
            #     9:00:00.000
            #     9:00:00.500
            #     9:00:01.000
            #     9:00:01.500
            #     ...
            #
            # This algorithm is proposed by luyiming.

            second_list = np.empty((len(day_info.tick) + 1,), dtype=np.int32)
            milsecond_list = np.empty((len(day_info.tick) + 1,),
                                      dtype=np.int32)
            second_list[1:] = time_list / 1000
            # NOTE(reed): We never touch the first time.
            second_list[0] = second_list[1] - 1

            milsecond_list[1:] = time_list % 100000
            milsecond_list[0] = milsecond_list[1]

            second_diff = second_list[1:] - second_list[:-1]
            milsecond_diff = milsecond_list[1:] - milsecond_list[:-1]

            wrong_time_indexes = np.all(
                np.stack([second_diff == 0, milsecond_diff < 500]), axis=0)

            # There are some timestamps need to be modified.
            if wrong_time_indexes.any():
                time_list[wrong_time_indexes] += (
                    500 - milsecond_diff[wrong_time_indexes])

        today = str(element['TradingDay'])
        yestoday = (pd.Timestamp(today) + dtime.timedelta(days=-1)) \
            .strftime('%Y%m%d')

        def translate_time(itime, today=today, yestoday=yestoday):
            """
            translate time from int to string
            """
            # print('%s type %s' % (itime, type(itime)))
            stime = str(int(itime)).zfill(9)
            stime = stime[0:2]+':'+stime[2:4]+':'+stime[4:6]+'.'+stime[6:]
            # 银河数据集的夜盘数据是直接放在该交易日的开头的
            # 比如： 21:00:01, 21:00:21 ...... 22:59:59.500, 09:00:00.000 ......
            # 为了之后get_day_bar填充方便， 我们把当天0点之前的夜盘的日期改为yestoday
            # 我们用收盘后下午7点作为夜盘的分隔(当然3,4,5,6点都可以)
            if itime > 190000000:
                stime = yestoday + ' ' + stime
            else:
                stime = today + ' ' + stime
            try:
                return pd.Timestamp(stime)
            except:
                # print itime, today
                # 股票中有秒数超过60的现象
                return None
        df = pd.DataFrame(filedata, columns=expand_columns)
        # 将-1赋值为nan
        df[df == -1] = pd.np.nan

        # Set datetime and index.
        df['datetime'] = map(translate_time, time_list)

        # 将股票数据中的错误时间点行删掉
        # 删除股票错误时间点需放在检查的前面， 不然做diff的时候
        # 会出现两个None不能相减的情况
        df.drop(df.index[pd.isnull(df.datetime)], inplace=True)

        # NOTE(reed): This should be comment out when fully tested.
        if not np.all(df['datetime'].diff().dropna().as_matrix()
                      .astype(np.int64) >= 0):
            logger.warn("time is not monotonically increasing")
        df.set_index('datetime', inplace=True)

        first_time = df.index[-1]
        today = first_time.normalize()
        if pad:
            is_futures = _is_futures(instrument_id)
            assert is_futures, "padding is not supported for stocks now."
            freq = '500ms'

            # TODO(reed): Using last value isn't suitable for all other
            # columns, but for Futures it's enough now. CHECK IT LATER.
            df = df.resample(freq).last().fillna(method='pad')

            # Filter data according to the trading time.
            # 开始支持夜盘， 不再传入time_type
            # rest_time_list = _get_rest_time(instrument_id, today, time_type)
            rest_time_list = _get_rest_time(instrument_id, today)
            # NOTE(reed): All columns share the same index, so we just use the
            # last col to generate index.
            for start, end in rest_time_list:
                df.drop(
                    df.index[(df.index >= start) & (df.index < end)],
                    inplace=True)

        # 统一赋值instrument_id, 日夜盘标志与时间
        if 'instrument_id' in expand_columns:
            df['instrument_id'] = instrument_id
        # TODO(lym): 日夜盘的标志目前暂时不管，之后再完善
        if 'type' in expand_columns:
            df['type'] = time_type
        # NOTE(reed): volume and turnover should use acc_volume, acc_turnover
        # to calculate for tick data.
        # TODO(reed): Should we take the first acc_volume as the first volume?
        if 'volume' in expand_columns:
            df['volume'] = df['acc_volume'].diff().fillna(
                df['acc_volume'].iloc[0], limit=1)
        if 'turnover' in expand_columns:
            df['turnover'] = df['acc_turnover'].diff().fillna(
                df['acc_turnover'].iloc[0], limit=1)

        # 对所有的价格除以10000
        df[local_price_list] /= 10000
        # 对于取部分数据的要求进行处理
        # index_date = list(df.index)
        # df_np = df.as_matrix()
        # if pad:
        #     morningbegin = today + pd.to_timedelta('09:00:00')
        #     afternoonbegin = today + pd.to_timedelta('13:30:00')
        # else:
        #     morningbegin = today + pd.to_timedelta(morningbegin)
        #     try:
        #         afternoonbegin = today + pd.to_timedelta(afternoonbegin)
        #     except:
        #         pass

        morningbegin = today + pd.to_timedelta('08:00:00')
        afternoonbegin = today + pd.to_timedelta('12:30:00')

        if indaymerge:
            if indayperiod[0] == MORNING:
                df = df[morningbegin:]
            elif indayperiod[0] == AFTERNOON:
                df = df[afternoonbegin:]
            result.append(df)
        else:
            # 要求不同时间段分割返回
            # 由于已经drop掉了多余的数据， 这里的时间范围可以放宽一点
            # 以兼容股指期货和商品期货
            nightdata = df[:morningbegin]
            morningdata = df[morningbegin: afternoonbegin]
            afternoondata = df[afternoonbegin:]
            if indayperiod[-1] == NIGHT:
                result.append([nightdata, ])
            if indayperiod[-1] == MORNING:
                if len(indayperiod) == 1:
                    result.append([morningdata, ])
                else:
                    result.append([nightdata, morningdata])
            if indayperiod[-1] == AFTERNOON:
                if len(indayperiod) == 1:
                    result.append([afternoondata, ])
                if len(indayperiod) == 2:
                    result.append([morningdata, afternoondata])
                if len(indayperiod) == 3:
                    result.append([nightdata, morningdata, afternoondata])
            # try:
            #     pos1 = index_date.index(morningbegin)
            # except:
            #     pos1 = -1
            # try:
            #     pos2 = index_date.index(afternoonbegin)
            # except:
            #     pos2 = -1
            # # TODO(lym): 比较一下用iloc和 dataframe-->numpy-->检索
            # #            -->dataframe的速度
            # if indayperiod[-1] == NIGHT:
            #     result.append(df)
            #     # return result
            # if indayperiod[-1] == MORNING:
            #     if len(indayperiod) == 1:
            #         result.append([df.iloc[pos1:], ])
            #         # return result
            #     else:
            #         result.append([df.iloc[:pos1], df.iloc[pos1:]])
            #         # return result
            # if indayperiod[-1] == AFTERNOON:
            #     if len(indayperiod) == 1:
            #         result.append([df.iloc[pos2:], ])
            #         # return result
            #     if len(indayperiod) == 2:
            #         result.append([df.iloc[pos1:pos2], df.iloc[pos2:]])
            #         # return result
            #     if len(indayperiod) == 3:
            #         result.append([df.iloc[:pos1], df.iloc[pos1:pos2],
            #                       df.iloc[pos2:]])
            #         # return result
    return result


if __name__ == "__main__":
    print('begin')

    k1 = get_stock_factor('11', 20150609)
    print k1

    # 1.1. get_day_tick用法1： 传入一组日期
    c1 = get_day_tick('cu', 20160805, data_source=YINHE, pad=True,
                      indayperiod=[MORNING, AFTERNOON])
    t0 = get_day_tick('002566.SZ', (20160101, 20161231))
    tt1 = time.time()
    t1 = get_day_bar('rb', (20140101, 20141222), merge=False,
                     data_source=YINHE, indayperiod=ALL_PERIOD,
                     indaymerge=True, freq='3S')
    tt1_1 = time.time()
    print "bar test"
    print "cost time: ", tt1_1-tt1

    # 1.1. get_day_tick用法1： 传入一组日期
    tt1 = time.time()
    t1 = get_day_tick('rb', (20140101, 20141222), merge=False,
                      data_source=YINHE)
    tt1_1 = time.time()
    print "tick test"
    print "cost time: ", tt1_1-tt1

    # 1.2. get_day_tick用法2： 传入一个“开始--终止”日期
    #   的元组， 检索出改时间段的tick数据后返回
    print 'get t2'
    tt1 = time.time()
    t2 = get_day_tick('if1405', (20140322, 20140326))
    tt2 = time.time()
    print('spend time ' + str(tt2-tt1))
    print t2.index[0]
    print t2.index[-1]

    # 1.3. get_day_tick用法3： 传入一个日期
    #   检索出该日期的tick数据并返回
    print 'get t3'
    tt1 = time.time()
    t3 = get_day_tick('if1405', 20140505, ['interest'])
    tt2 = time.time()
    print t3.index[0]
    print t3.index[-1]
    print('spend time ' + str(tt2-tt1))

    # 1.4. get_day_tick用法4：只传入期货类型代码表示获取“主力合约”
    print 'get t4'
    tt1 = time.time()
    t4 = get_day_tick(
        'if', [20140322, 20140323, 20140401],
        ['interest', 'instrument_id', 'type'])
    tt2 = time.time()
    print('spend time ' + str(tt2-tt1))
    print t4.index[0], t4.instrument_id[0], t4.type[0]
    print t4.index[-1]

    # 1.5. get_day_tick用法5：只传入期货类型代码表示获取“主力合约”
    print 'get t5'
    tt1 = time.time()
    t5 = get_day_tick('if', (20140322, 20140326))
    tt2 = time.time()
    print('spend time ' + str(tt2-tt1))
    print t5.index[0], t5.instrument_id[0]
    print t5.index[-1]

    # 1.6. get_day_tick用法6：只传入期货类型代码表示获取“主力合约”, 取得数据大
    # 于4天,使用多进程.
    print 'get t6'
    tt1 = time.time()
    t6 = get_day_tick('if', (20140322, 20140426))
    tt2 = time.time()
    print('spend time ' + str(tt2-tt1))
    print t6.index[0], t6.instrument_id[0]
    print t6.index[-1]

    # 1.7. get_day_tick用法7：只传入期货类型代码表示获取“主力合约”, 取得数据大
    # 于4天,使用多进程, 并且对数据进行padding.
    print 'get t7'
    tt1 = time.time()
    t7 = get_day_tick('if', (20140322, 20140426), data_source=YINHE, pad=True)
    tt2 = time.time()
    print('spend time ' + str(tt2-tt1))
    print t7.index[0], t7.instrument_id[0]
    print t7.index[-1]

    # 2.1. get_day_bar用法1: 取得分钟级k线数据
    print 'get b1'
    tt1 = time.time()
    b1 = get_day_bar('if', (20100416, 20100420), freq='1T', data_source=YINHE)
    tt2 = time.time()
    print('spend time ' + str(tt2-tt1))
    print b1.index[0], b1.instrument_id[0]
    print b1.index[-1]

    # 2.2. get_day_bar用法2: 取得5分钟级k线数据
    print 'get b2'
    tt1 = time.time()
    b2 = get_day_bar('if', (20100416, 20100420), freq='5T', data_source=YINHE)
    tt2 = time.time()
    print('spend time ' + str(tt2-tt1))
    print b2.index[0], b2.instrument_id[0]
    print b2.index[-1]

    # 2.3. get_day_bar用法3: 取得天级k线数据
    print 'get b3'
    tt1 = time.time()
    b3 = get_day_bar('if', (20140101, 20140131), freq='D', data_source=YINHE)
    tt2 = time.time()
    print('spend time ' + str(tt2-tt1))
    print b3.index[0], b3.instrument_id[0]
    print b3.index[-1]

    # 2.4. get_day_bar用法4: 取得周级k线数据
    print 'get b4'
    tt1 = time.time()
    b4 = get_day_bar('if', (20140101, 20140131), freq='W', data_source=YINHE)
    tt2 = time.time()
    print('spend time ' + str(tt2-tt1))
    print b4.index[0], b4.instrument_id[0]
    print b4.index[-1]

    # 2.5. get_day_bar用法5: 取得月级k线数据
    print 'get b5'
    tt1 = time.time()
    b5 = get_day_bar('if', (20140101, 20140331), freq='M', data_source=YINHE)
    tt2 = time.time()
    print('spend time ' + str(tt2-tt1))
    print b5.index[0], b5.instrument_id[0]
    print b5.index[-1]

    # 注： 返回的数据类型为pandas的DataFrame，其中column的字段在tick.proto文件
    #      中全部有标示。 不过返回值做了改动，有下列几点：
    #   1. 价格相关的都已经是真实的的价格--float型，不再是proto文件中的INT型
    #   2. time已经转换为pandas.Timestamp类型，并且包含了日期信息（20150102 10:30:25.332）
    #   3. proto中有些字段没有值(交易所没有提供), 全部用numpy模块的NaN替代
    #   4. 加了一个instrument_id字段（即合约号，如IF1601）
    #   5. 加了一个type字段表示日夜盘 0：日盘   1：夜盘

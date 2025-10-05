# 获取期权数据
import pandas as pd
import json
import requests
from bs4 import BeautifulSoup
import datetime
from dateutil.relativedelta import relativedelta
import calendar

# GET请求头(根据反反爬需要可调整)
http_header = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Host': 'hq.sinajs.cn',
    'Referer': 'https://stock.finance.sina.com.cn/',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'script',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
}

# 隐藏requests关于ssl证书的警告
requests.packages.urllib3.disable_warnings()

'''
API参数说明:
exchange - 含义
'上交所'/'null' - 上交所
'深交所' - 深交所
'''


# 某交易所期权的合约月份
def get_y_m(exchange):
    res = []
    time = datetime.date.today()

    # 到期日已结束
    _, t = get_d(exchange, time.strftime('%Y-%m'))
    if t < 0:
        time += relativedelta(months=1)

    res.append(time.strftime('%Y-%m'))

    # 中金所期权合约月份: 当月、下2个月及随后3个季月
    if exchange == '中金所':
        for i in range(2):
            time += relativedelta(months=1)
            res.append(time.strftime('%Y-%m'))
        y = time.year
        m = time.month
        if m < 3:  # 下一个季月
            m = 3
        elif m < 6:
            m = 6
        elif m < 9:
            m = 9
        elif m < 12:
            m = 12
        else:
            y += 1
            m = 3
        time = datetime.date(y, m, 1)
        res.append(time.strftime('%Y-%m'))
        for i in range(2):
            time += relativedelta(months=3)
            res.append(time.strftime('%Y-%m'))
        return res

    # 上交所, 深交所期权合约月份: 当月、下月及随后两个季月
    time += relativedelta(months=1)
    res.append(time.strftime('%Y-%m'))
    y = time.year
    m = time.month
    if m < 3:  # 下一个季月
        m = 3
    elif m < 6:
        m = 6
    elif m < 9:
        m = 9
    elif m < 12:
        m = 12
    else:
        y += 1
        m = 3
    time = datetime.date(y, m, 1)
    res.append(time.strftime('%Y-%m'))
    time += relativedelta(months=3)
    res.append(time.strftime('%Y-%m'))
    return res


'''
上交所, 深交所期权合约月份:
r = requests.get('http://stock.finance.sina.com.cn/futures/api/openapi.php/StockOptionService.getStockName?exchange=' + exchange)
return json.loads(r.text)['result']['data']['contractMonth']
'''


# 某交易所某合约月份的到期日 & 剩余天数
def get_d(exchange, date):
    # 中金所期权到期日: 到期月份的第三个星期五(遇国家法定假日顺延, 暂不考虑)
    if exchange == '中金所':
        time = datetime.date.fromisoformat(date + '-01')
        c = calendar.Calendar(firstweekday=calendar.SUNDAY)
        monthcal = c.monthdatescalendar(time.year, time.month)
        third_friday = [day
                        for week in monthcal
                        for day in week
                        if day.weekday() == calendar.FRIDAY and day.month == time.month][2]
        return third_friday.strftime('%Y-%m-%d'), (third_friday - datetime.date.today()).days
    # 上交所, 深交所期权到期日: 到期月份的第四个星期三(遇国家法定假日顺延, 暂不考虑)
    time = datetime.date.fromisoformat(date + '-01')
    c = calendar.Calendar(firstweekday=calendar.SUNDAY)
    monthcal = c.monthdatescalendar(time.year, time.month)
    fourth_wednesday = [day
                        for week in monthcal
                        for day in week
                        if day.weekday() == calendar.WEDNESDAY and day.month == time.month][3]
    return fourth_wednesday.strftime('%Y-%m-%d'), (fourth_wednesday - datetime.date.today()).days


'''
上交所, 深交所期权到期日 & 剩余天数(除权日暂不考虑)
r = requests.get('http://stock.finance.sina.com.cn/futures/api/openapi.php/StockOptionService.getRemainderDay?exchange=null&date=' + date)
return json.loads(r.text)['result']['data']['expireDay'], json.loads(r.text)['result']['data']['remainderDays']
'''

'''
API参数说明:
code - 含义
'510050' - 上交所50ETF
'510300' - 上交所300ETF
'510500' - 上交所500ETF
'159901' - 深交所深证100ETF
'159915' - 深交所创业板ETF
'159919' - 深交所沪深300ETF
'159922' - 深交所中证500ETF
'''


# y年m月到期的看涨期权代码列表(code为股票代码, y_m均为合约月份)(适用于上交所, 深交所)
def get_up_options(code, y_m):
    r = requests.get('https://hq.sinajs.cn/list=OP_UP_' + code + y_m, headers=http_header, verify=False)
    data = r.text.split('"')[1]
    return data


# y年m月到期的看跌期权代码列表(code为股票代码, y_m均为合约月份)(适用于上交所, 深交所)
def get_down_options(code, y_m):
    r = requests.get('https://hq.sinajs.cn/list=OP_DOWN_' + code + y_m, headers=http_header, verify=False)
    data = r.text.split('"')[1]
    return data


# 示例: zl查询主力合约信息(list为期权代码数字部分)(适用于上交所, 深交所)
def get_zl(list):
    r = requests.get('https://hq.sinajs.cn/list=CON_ZL_' + list, headers=http_header)
    data = r.text.split('"')[1].split(',')

    header = ['合约简称', '', '', '', '持仓量', '持仓量占比', '最新价', '最新价涨幅', '买价', '卖价', '最高价', '最低价', '成交量',
              'Delta', 'Gamma', 'Theta', 'Vega', '隐含波动率', '交易代码', '行权价', '理论价值', '虚实值标志']
    return dict(zip(header, data))


# 示例: so查询合约信息(list为期权代码数字部分)(适用于上交所, 深交所)
def get_so(list):
    r = requests.get('https://hq.sinajs.cn/list=CON_SO_' + list, headers=http_header)
    data = r.text.split('"')[1].split(',')

    header = ['合约简称', '', '', '', '成交量', 'Delta', 'Gamma', 'Theta', 'Vega', '隐含波动率', '最高价', '最低价', '交易代码',
              '行权价', '最新价', '理论价值', '虚实值标志']
    return dict(zip(header, data))


# 示例: op查询合约详细信息(list为期权代码数字部分)(适用于上交所, 深交所)
# (中金所股票期权 / 商品期权: 将'CON'改为'P', 数据到'认购认沽标志'前(含), 且有部分缺失)
def get_op(list):
    r = requests.get('https://hq.sinajs.cn/list=CON_OP_' + list, headers=http_header)
    data = r.text.split('"')[1].split(',')

    header = ['买量', '买价', '最新价', '卖价', '卖量', '持仓量', '涨跌幅', '行权价', '昨收价', '开盘价', '涨停价', '跌停价',
              '申卖价五', '申卖量五', '申卖价四', '申卖量四', '申卖价三', '申卖量三', '申卖价二', '申卖量二', '申卖价一', '申卖量一',
              '申买价一', '申买量一', '申买价二', '申买量二', '申买价三', '申买量三', '申买价四', '申买量四', '申买价五', '申买量五',
              '行情时间', '主力合约标识', '状态码', '标的证券类型', '标的股票', '合约简称', '振幅', '最高价', '最低价',
              '成交量', '成交额', '分红调整标志', '昨结算价', '认购认沽标志', '到期日', '剩余天数', '虚实值标志', '内在价值', '时间价值']
    return dict(zip(header, data))


# 查询基础信息, 返回T型报价 & 看涨期权的虚实值标志(list1为看涨期权代码列表, list2为看跌期权代码列表)
def get_basic(list1, list2):
    # 提取看涨期权的'持仓量', '成交量', '卖量', '卖价', '买量', '买价', '涨幅', '最新价', '行权价'
    r = requests.get('https://hq.sinajs.cn/list=' + list1, headers=http_header, verify=False)
    data = r.text.split('"')
    res = []
    flag = []
    i = 1
    while i < len(data):
        t = data[i].split(',')
        if len(t) < 42:  # 查询出错
            return None, None
        res.append([t[5], t[41], t[4], t[3], t[0], t[1], t[6], t[2], t[7]])
        if len(t) > 48:  # 除中金所外
            flag.append(t[48])  # 记录看涨期权的虚实值标志
            if t[43] != 'M':  # 在行权价后插入分红调整标志
                res[-1][-1] += t[43]
        i += 2

    # 反向插入看跌期权的~
    r = requests.get('https://hq.sinajs.cn/list=' + list2, headers=http_header, verify=False)
    data = r.text.split('"')
    i = 1
    j = 0
    while i < len(data) and j < len(res):
        t = data[i].split(',')
        res[j] += [t[2], t[6], t[1], t[0], t[3], t[4], t[41], t[5]]
        i += 2
        j += 1

    return res, flag


# T型报价查询, 返回期权代码代表 & T型报价 & 看涨期权的虚实值标志(pinzhong为期权品种, y_m均为合约月份)(适用于上交所, 深交所)
def get_msg_1(pinzhong, y_m):
    up_list = get_up_options(pinzhong, y_m)
    down_list = get_down_options(pinzhong, y_m)
    list = (up_list + down_list).replace('CON_OP_', '').split(',')
    list.remove('')
    data, flag = get_basic(up_list, down_list)
    return list, data, flag


# T型报价查询, 返回期权代码代表 & T型报价(product为期权品种, y_m均为合约月份)(适用于中金所)
def get_msg_2(product, y_m):
    r = requests.get(
        'http://stock.finance.sina.com.cn/futures/api/openapi.php/OptionService.getOptionData?type=futures&product=' + product + '&exchange=cffex&pinzhong=' + product + y_m)
    data = json.loads(r.text)['result']['data']

    list = []
    up_list = ''
    for i in data['up']:
        list.append(i[-1])
        t = 'P_OP_' + i[-1]
        up_list += t + ','
    down_list = ''
    for i in data['down']:
        list.append(i[-1])
        t = 'P_OP_' + i[-1]
        down_list += t + ','

    res, _ = get_basic(up_list, down_list)

    for i in range(len(res)):
        res[i][6] = str(data['up'][i][6])  # 补充缺失的'涨幅数据'
        res[i][10] = str(data['down'][i][6])
        res[i][0] = res[i][0][0:-4]  # 持仓量保留整数部分
        res[i][-1] = res[i][-1][0:-4]

    return list, res, None


# 查询详细信息, 返回分类报价(list为期权代码列表)
def get_long(list):
    code_list = list.split(',')
    code_list.remove('')

    # op查询: '合约代码', '合约简称', '涨幅', '最新价', '买价', '卖价', '买量', '卖量', '持仓量', '成交量', '成交额', '振幅'
    r = requests.get('https://hq.sinajs.cn/list=' + list, headers=http_header, verify=False)
    data_op = r.text.split('"')

    res = []
    i = 1
    list_idx = 0
    while list_idx < len(code_list):
        item = []
        item.append(code_list[list_idx][7::])
        t = data_op[i].split(',')
        if len(t) < 43:  # 查询出错
            return None
        item += [t[37], t[6], t[2], t[1], t[3], t[0], t[4], t[5], t[41], t[42], t[38] + '%']
        res.append(item)
        i += 2
        list_idx += 1

    # so查询: 'Delta', 'Gamma', 'Theta', 'Vega', '隐含波动率'
    r = requests.get('https://hq.sinajs.cn/list=' + list.replace('OP', 'SO'), headers=http_header, verify=False)
    data_so = r.text.split('"')

    i = 1
    list_idx = 0
    while list_idx < len(code_list):
        t = data_so[i].split(',')
        if len(t) < 10:  # 查询出错
            return None
        res[list_idx] += [t[5], t[6], t[7], t[8], t[9]]
        i += 2
        list_idx += 1

    return res


# 分类报价查询(适用于上交所, 深交所)
def get_msg_l(exchange):
    dict = {'上交所': ['510050', '510300', '510500'],
            '深交所': ['159901', '159915', '159919', '159922']}
    list = ''
    for y_m in get_y_m(exchange):
        for pinzhong in dict[exchange]:
            y_m = y_m[2::].replace('-', '')
            list += get_up_options(pinzhong, y_m)
            list += get_down_options(pinzhong, y_m)

    res = get_long(list)
    res.sort(key=lambda x: x[0])  # 按照合约代码排序

    # 深交所缺失的数据
    if exchange == '深交所':
        funa = lambda x: '-' if x == '0' else x
        funb = lambda x: '-' if x == 'NAN' else x
        for i in range(len(res)):
            res[i][12] = funa(res[i][12])
            res[i][13] = funb(res[i][13])
            res[i][14] = funa(res[i][14])
            res[i][15] = funa(res[i][15])

    return res


# 查询期权合约详细信息(op == 'CON': 上交所, 深交所股票期权; op == 'P': 中金所股票期权 / 商品期权)
def get_detail(op, code):
    r = requests.get('https://hq.sinajs.cn/list=' + op + '_OP_' + code, headers=http_header, verify=False)
    data = r.text.split('"')[1].split(',')
    # 期权合约不存在
    if len(data) == 1:
        return -1, None, None, None
    if op == 'CON':
        # 基础数据:
        # 0合约简称, 1标的股票, 2合约类型, 3到期日, 4剩余天数, \
        # 5价值状态,
        # 6买量, 7买价, 8卖量, 9卖价, 10最新价, 11行权价,
        # 12最高价, 13最低价, 14昨收价, 15开盘价, 16涨停价, 17跌停价,
        # 18涨幅, 19振幅, 20持仓量, 21成交量, 22成交额, 23分红调整,
        # 24申买量一, 25申买量二, 26申买量三, 27申买量四, 28申买量五,
        # 29申买价一, 30申买价二, 31申买价三, 32申买价四, 33申买价五,
        # 34申卖量一, 35申卖量二, 36申卖量三, 37申卖量四, 38申卖量五,
        # 39申卖价一, 40申卖价二, 41申卖价三, 42申卖价四, 43申卖价五
        if data[6] != '':
            data[6] += '%'
        if data[38] != '':
            data[38] += '%'
        text1 = [data[37], data[36], data[48].replace('2', '认购').replace('1', '认沽'), data[49], data[50],
                 data[48].replace('1', '虚值').replace('2', '实值'),
                 data[0], data[1], data[4], data[3], data[2], data[7],
                 data[39], data[40], data[8], data[9], data[10], data[11],
                 data[6], data[38], data[5], data[41], data[42], data[43],
                 data[23], data[25], data[27], data[29], data[31],
                 data[22], data[24], data[26], data[28], data[30],
                 data[13], data[15], data[17], data[19], data[21],
                 data[12], data[14], data[16], data[18], data[20]
                 ]
        # 价值分析:
        # 0最新价, 1时间价值, 2内在价值
        text2 = [data[2], data[50], data[49]]
        # 风险分析:
        # 0涨幅, 1振幅
        text3 = [data[6] + '%', data[38] + '%']

        r = requests.get('https://hq.sinajs.cn/list=' + op + '_SO_' + code, headers=http_header, verify=False)
        data = r.text.split('"')[1].split(',')
        # 价值分析:
        # 3隐含波动率, 4理论价值
        text2 += [data[9], data[15]]
        # 风险分析:
        # 2Delta, 3Gamma, 4Theta, 5Vega,
        # 6行权概率
        text3 += [data[5], data[6], data[7], data[8]]
        delta = float(data[5]) * 100
        if delta < 0:
            delta = -delta
        text3 += [format(delta, '.2f') + '%']

        for i in range(len(text1)):
            if text1[i] == '':
                text1[i] = '-'
        for i in range(len(text2)):
            if text2[i] == '':
                text2[i] = '-'
        for i in range(len(text3)):
            if text3[i] == '':
                text3[i] = '-'

        return 1, text1, text2, text3

    else:
        # 基础数据:
        # 0买量, 1买价, 2卖量, 3卖价, 4最新价, 5行权价,
        # 6最高价, 7最低价, 8昨收价, 9开盘价, 10涨停价, 11跌停价,
        # 12涨幅, 13持仓量, 14成交量, 15成交额,
        # 16申买量一, 17申买量二, 18申买量三, 19申买量四, 20申买量五,
        # 21申买价一, 22申买价二, 23申买价三, 24申买价四, 25申买价五,
        # 26申卖量一, 27申卖量二, 28申卖量三, 29申卖量四, 30申卖量五,
        # 31申卖价一, 32申卖价二, 33申卖价三, 34申卖价四, 35申卖价五
        if data[6] != '':
            data[6] += '%'
        text1 = [data[0], data[1], data[4], data[3], data[2], data[7],
                 data[39], data[40], data[8], data[9], data[10], data[11],
                 data[6], data[5], data[41], data[42],
                 data[23], data[25], data[27], data[29], data[31],
                 data[22], data[24], data[26], data[28], data[30],
                 data[13], data[15], data[17], data[19], data[21],
                 data[12], data[14], data[16], data[18], data[20]
                 ]

        for i in range(len(text1)):
            if text1[i] == '':
                text1[i] = '-'

    return 2, text1, None, None


# 查询日K(op == 'CON': 上交所, 深交所股票期权; op == 'P': 中金所股票期权 / 商品期权)
def get_dayline(op, code):
    if op == 'CON':
        r = requests.get(
            'http://stock.finance.sina.com.cn/futures/api/jsonp_v2.php//StockOptionDaylineService.getSymbolInfo?symbol=' + code)
        data = r.text.split('(')[1].split(')')[0]
        return json.loads(data)
    r = requests.get(
        'https://stock.finance.sina.com.cn/futures/api/jsonp.php//FutureOptionAllService.getOptionDayline?symbol=' + code)
    data = r.text.split('(')[1].split(')')[0]
    return json.loads(data)


# 查询分时线(仅适用于op == 'CON')
def get_hourline(code):
    r = requests.get(
        'https://stock.finance.sina.com.cn/futures/api/openapi.php/StockOptionDaylineService.getOptionMinline?symbol=CON_OP_' + code)
    data = json.loads(r.text)['result']['data']
    return data


# 查询商品期权的到期年月(from akshare)
def option_commodity_contract_sina(symbol: str = "玉米期权") -> pd.DataFrame:
    '''
    当前可以查询的期权品种的合约日期
    https://stock.finance.sina.com.cn/futures/view/optionsDP.php
    :param symbol: choice of {"豆粕期权", "玉米期权", "铁矿石期权", "棉花期权", "白糖期权", "PTA期权", "甲醇期权", "橡胶期权", "沪铜期权", "黄金期权", "菜籽粕期权", "液化石油气期权", "动力煤期权", "菜籽油期权", "花生期权"}
    :type symbol: str
    :return: e.g., {'黄金期权': ['au2012', 'au2008', 'au2010', 'au2104', 'au2102', 'au2106', 'au2108']}
    :rtype: dict
    '''
    url = (
        'https://stock.finance.sina.com.cn/futures/view/optionsDP.php/pg_o/dce'
    )
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    url_list = [
        item.find('a')['href']
        for item in soup.find_all('li', attrs={'class': 'active'})
        if item.find('a') is not None
    ]
    commodity_list = [
        item.find('a').text
        for item in soup.find_all('li', attrs={'class': 'active'})
        if item.find('a') is not None
    ]
    comm_list_dict = {
        key: value for key, value in zip(commodity_list, url_list)
    }
    url = 'https://stock.finance.sina.com.cn' + comm_list_dict[symbol]
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    symbol = (
        soup.find(attrs={'id': 'option_symbol'})
            .find(attrs={'class': 'selected'})
            .text
    )
    contract = [
        item.text
        for item in soup.find(attrs={'id': 'option_suffix'}).find_all('li')
    ]
    temp_df = pd.DataFrame({symbol: contract})
    temp_df.reset_index(inplace=True)
    temp_df['index'] = temp_df.index + 1
    temp_df.columns = ['序号', '合约']
    return temp_df


# 查询商品期权的T型报价(from akshare)
def option_commodity_contract_table_sina(
        symbol: str = '黄金期权', contract: str = 'au2204'
) -> pd.DataFrame:
    '''
    当前所有期权合约, 包括看涨期权合约和看跌期权合约
    https://stock.finance.sina.com.cn/futures/view/optionsDP.php
    :param symbol: choice of {"豆粕期权", "玉米期权", "铁矿石期权", "棉花期权", "白糖期权", "PTA期权", "甲醇期权", "橡胶期权", "沪铜期权", "黄金期权", "菜籽粕期权", "液化石油气期权", "动力煤期权", "菜籽油期权", "花生期权"}
    :type symbol: str
    :param contract: e.g., 'au2012'
    :type contract: str
    :return: 合约实时行情
    :rtype: pandas.DataFrame
    '''
    url = (
        'https://stock.finance.sina.com.cn/futures/view/optionsDP.php/pg_o/dce'
    )
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    url_list = [
        item.find('a')['href']
        for item in soup.find_all('li', attrs={'class': 'active'})
        if item.find('a') is not None
    ]
    commodity_list = [
        item.find('a').text
        for item in soup.find_all('li', attrs={'class': 'active'})
        if item.find('a') is not None
    ]
    comm_list_dict = {
        key: value for key, value in zip(commodity_list, url_list)
    }
    url = 'https://stock.finance.sina.com.cn/futures/api/openapi.php/OptionService.getOptionData'
    params = {
        'type': 'futures',
        'product': comm_list_dict[symbol].split('/')[-2],
        'exchange': comm_list_dict[symbol].split('/')[-1],
        'pinzhong': contract,
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    up_df = pd.DataFrame(data_json['result']['data']['up'])
    down_df = pd.DataFrame(data_json['result']['data']['down'])
    temp_df = pd.concat([up_df, down_df], axis=1)
    temp_df.columns = [
        '看涨合约-买量',
        '看涨合约-买价',
        '看涨合约-最新价',
        '看涨合约-卖价',
        '看涨合约-卖量',
        '看涨合约-持仓量',
        '看涨合约-涨跌',
        '行权价',
        '看涨合约-看涨期权合约',
        '看跌合约-买量',
        '看跌合约-买价',
        '看跌合约-最新价',
        '看跌合约-卖价',
        '看跌合约-卖量',
        '看跌合约-持仓量',
        '看跌合约-涨跌',
        '看跌合约-看跌期权合约',
    ]
    temp_df['看涨合约-买量'] = pd.to_numeric(temp_df['看涨合约-买量'], errors='coerce')
    temp_df['看涨合约-买价'] = pd.to_numeric(temp_df['看涨合约-买价'], errors='coerce')
    temp_df['看涨合约-最新价'] = pd.to_numeric(temp_df['看涨合约-最新价'], errors='coerce')
    temp_df['看涨合约-卖价'] = pd.to_numeric(temp_df['看涨合约-卖价'], errors='coerce')
    temp_df['看涨合约-卖量'] = pd.to_numeric(temp_df['看涨合约-卖量'], errors='coerce')
    temp_df['看涨合约-持仓量'] = pd.to_numeric(temp_df['看涨合约-持仓量'], errors='coerce')
    temp_df['看涨合约-涨跌'] = pd.to_numeric(temp_df['看涨合约-涨跌'], errors='coerce')
    temp_df['行权价'] = pd.to_numeric(temp_df['行权价'], errors='coerce')
    temp_df['看跌合约-买量'] = pd.to_numeric(temp_df['看跌合约-买量'], errors='coerce')
    temp_df['看跌合约-买价'] = pd.to_numeric(temp_df['看跌合约-买价'], errors='coerce')
    temp_df['看跌合约-最新价'] = pd.to_numeric(temp_df['看跌合约-最新价'], errors='coerce')
    temp_df['看跌合约-卖价'] = pd.to_numeric(temp_df['看跌合约-卖价'], errors='coerce')
    temp_df['看跌合约-卖量'] = pd.to_numeric(temp_df['看跌合约-卖量'], errors='coerce')
    temp_df['看跌合约-持仓量'] = pd.to_numeric(temp_df['看跌合约-持仓量'], errors='coerce')
    temp_df['看跌合约-涨跌'] = pd.to_numeric(temp_df['看跌合约-涨跌'], errors='coerce')
    return temp_df


# 查询价值潜力榜(B, S, V分别为买量, 卖量, 成交量阈值)
def get_msg_rank(B, S, V):
    exchange_list = ['上交所', '深交所']
    dict = {'上交所': ['510050', '510300', '510500'],
            '深交所': ['159901', '159915', '159919', '159922']}
    list = ''
    for exchange in exchange_list:
        for y_m in get_y_m(exchange):
            for pinzhong in dict[exchange]:
                y_m = y_m[2::].replace('-', '')
                list += get_up_options(pinzhong, y_m)
                list += get_down_options(pinzhong, y_m)

    code_list = list.split(',')
    code_list.remove('')
    list_final = ''

    # op查询: '合约代码',
    # '合约简称', '标的股票', '涨幅', '最新价', '买价', '卖价', '买量', '卖量', '持仓量', '成交量', '振幅', '内在价值', '时间价值'
    r = requests.get('https://hq.sinajs.cn/list=' + list, headers=http_header, verify=False)
    data_op = r.text.split('"')

    res = []
    i = 1
    list_idx = 0
    while list_idx < len(code_list):
        t = data_op[i].split(',')
        if len(t) < 51:  # 查询出错
            return None
        if int(t[0]) >= B and int(t[4]) >= S and int(t[41]) >= V:
            list_final += code_list[list_idx] + ','
            item = []
            item.append(code_list[list_idx][7::])
            item += [t[37], t[36], t[6], t[2], t[1], t[3], t[0], t[4], t[5], t[41], t[38] + '%', t[49], t[50]]
            res.append(item)
        i += 2
        list_idx += 1

    # so查询: '行权概率', '隐含波动率', '价值潜力'
    r = requests.get('https://hq.sinajs.cn/list=' + list_final.replace('OP', 'SO'), headers=http_header, verify=False)
    data_so = r.text.split('"')

    i = 1
    list_idx = 0
    while list_idx < len(res):
        t = data_so[i].split(',')
        if len(t) < 16:  # 查询出错
            return None
        res[list_idx] += [t[5], t[9], format(float(t[15]) - float(res[list_idx][4]), '.2f')]
        i += 2
        list_idx += 1

    return res

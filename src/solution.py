# 为ui传递数据
import pandas as pd

import crawler

'''
股票期权:
上交所: http://www.sse.com.cn/
深交所: http://www.szse.cn/
中金所: http://www.cffex.com.cn/
'''


# 分类报价
def get_tableWidget_1(comboBox_ex_Text):
    return crawler.get_msg_l(comboBox_ex_Text)


# 交易所
def get_comboBox_ex12():
    return ['上交所', '深交所', '中金所']


# 期权品种
def get_comboBox_pz12(comboBox_ex12_Text):
    if comboBox_ex12_Text == '上交所':
        return ['50ETF', '300ETF', '500ETF']
    elif comboBox_ex12_Text == '深交所':
        return ['深证100ETF', '创业板ETF', '沪深300ETF', '中证500ETF']
    elif comboBox_ex12_Text == '中金所':
        return ['沪深300股指(IO)', '中证1000股指(MO)', '上证50股指(HO)']


# 合约月份
def get_comboBox_ym12(comboBox_ex12_Text):
    y_m = crawler.get_y_m(comboBox_ex12_Text)
    return y_m
    # res = []
    # [res.append(i) for i in y_m if i not in res]  # 去重
    # return res


# 到期日
def get_label_da12_text(comboBox_ex12_Text, comboBox_ym12_Text):
    return crawler.get_d(comboBox_ex12_Text, comboBox_ym12_Text)


# 标的资产
def get_label_ta12_text(comboBox_pz12_Text):
    dict = {'50ETF': '华夏上证50ETF(510050)',
            '300ETF': '华泰柏瑞沪深300ETF(510300)',
            '500ETF': '南方中证500ETF(510500)',
            '深证100ETF': '易方达深证100ETF(159901)',
            '创业板ETF': '易方达创业板ETF(159915)',
            '沪深300ETF': '嘉实沪深300ETF(159919)',
            '中证500ETF': '嘉实中证500ETF(159922)',
            '沪深300股指(IO)': '沪深300指数',
            '中证1000股指(MO)': '中证1000指数',
            '上证50股指(HO)': '上证50指数',
            }
    return dict[comboBox_pz12_Text]


# T型报价
def get_tableWidget_2(comboBox_pz12_Text, comboBox_ym12_Text):
    dict = {'50ETF': '510050',
            '300ETF': '510300',
            '500ETF': '510500',
            '深证100ETF': '159901',
            '创业板ETF': '159915',
            '沪深300ETF': '159919',
            '中证500ETF': '159922',
            '沪深300股指(IO)': 'io',
            '中证1000股指(MO)': 'mo',
            '上证50股指(HO)': 'ho',
            }
    code = dict[comboBox_pz12_Text]
    if len(code) <= 2:  # 中金所
        return crawler.get_msg_2(code, comboBox_ym12_Text[2::].replace('-', ''))
    else:
        return crawler.get_msg_1(code, comboBox_ym12_Text[2::].replace('-', ''))


'''
商品期权:
大商所: http://www.dce.com.cn/
上期所: https://www.shfe.com.cn/
郑商所: http://www.czce.com.cn/
广期所: http://www.gfex.com.cn/
'''


# 期权品种
def get_comboBox_pz21():
    return ['豆粕期权(M)', '玉米期权(C)', '液化石油气期权(PG)', '黄大豆1号期权(A)', '黄大豆2号期权(B)',
            '豆油期权(Y)', '铜期权(CU)', '螺纹钢期权(RB)', '黄金期权(AU)', '白银期权(AG)',
            '天然橡胶期权(RU)', '棉花期权(CF)', '菜籽油期权(OI)', '菜籽粕期权(RM)', '花生期权(PK)',
            'PTA期权(TA)', '甲醇期权(MA)', '动力煤期权(ZC)', '工业硅期权(SI)']


# 到期月份
def get_comboBox_ym21(comboBox_pz21_Index):
    list = ['豆粕期权', '玉米期权', '液化石油气期权', '黄大豆1号期权', '黄大豆2号期权',
            '豆油期权', '沪铜期权', '螺纹钢期权', '黄金期权', '白银期权',
            '橡胶期权', '棉花期权', '菜籽油期权', '菜籽粕期权', '花生期权',
            'PTA期权', '甲醇期权', '动力煤期权', '工业硅期权']
    data = crawler.option_commodity_contract_sina(symbol=list[comboBox_pz21_Index])
    res = data['合约'].values.tolist()
    res.sort()
    return res


# 交易所
def get_label_ex21_text(comboBox_pz21_Index):
    if comboBox_pz21_Index < 6:
        return '大商所'
    elif comboBox_pz21_Index < 11:
        return '上期所'
    elif comboBox_pz21_Index < 18:
        return '郑商所'
    else:
        return '广期所'


# T型报价
def get_tableWidget_3(comboBox_pz21_Index, comboBox_ym21_Text):
    list = ['豆粕期权', '玉米期权', '液化石油气期权', '黄大豆1号期权', '黄大豆2号期权',
            '豆油期权', '沪铜期权', '螺纹钢期权', '黄金期权', '白银期权',
            '橡胶期权', '棉花期权', '菜籽油期权', '菜籽粕期权', '花生期权',
            'PTA期权', '甲醇期权', '动力煤期权', '工业硅期权']
    # dict = {'大商所': 'dce',
    #         '上期所': 'shfe',
    #         '郑商所': 'czce',
    #         '广期所': 'gfex'}
    data = crawler.option_commodity_contract_table_sina(list[comboBox_pz21_Index], comboBox_ym21_Text)
    up_list = []
    down_list = []
    res = []
    for idx, row in data.iterrows():
        up_list.append(row['看涨合约-看涨期权合约'])
        down_list.append(row['看跌合约-看跌期权合约'])
        res.append(
            [str(row['看涨合约-持仓量']), str(row['看涨合约-卖量']), str(row['看涨合约-卖价']), str(row['看涨合约-买量']), str(row['看涨合约-买价']),
             str(row['看涨合约-涨跌']), str(row['看涨合约-最新价']), str(row['行权价']), str(row['看跌合约-最新价']), str(row['看跌合约-涨跌']),
             str(row['看跌合约-买价']), str(row['看跌合约-买量']), str(row['看跌合约-卖价']), str(row['看跌合约-卖量']), str(row['看跌合约-持仓量'])])
    return up_list + down_list, res


'''
合约分析
'''


# 合约详情
def get_tab_31(lineEdit_code_Text):
    # 合约代码 == ''
    if not len(lineEdit_code_Text):
        return 0, '', '', ''

    if lineEdit_code_Text[0] == '1' or lineEdit_code_Text[0] == '9':  # 上交所, 深交所股票期权
        op = 'CON'
    else:  # 中金所股票期权 / 商品期权
        op = 'P'
    flag, text1, text2, text3 = crawler.get_detail(op, lineEdit_code_Text)

    # 合约代码不存在
    if flag < 0:
        return -1, '', '', ''
    # 中金所股票期权 / 商品期权(无价值分析, 风险分析)
    if flag == 2:
        res1 = ('{:　<4}'.format('买量') + ': {t[0]: <10}' +  #
                '{:　<4}'.format('最高价') + ': {t[6]: <10}' +
                '{:　<4}'.format('涨幅') + ': {t[12]: <10}' +
                '{:　<4}'.format('申买量一') + ': {t[16]: <10}' +
                '{:　<4}'.format('申买价一') + ': {t[21]: <10}' +
                '{:　<4}'.format('申卖量一') + ': {t[26]: <10}' +
                '{:　<4}'.format('申卖价一') + ': {t[31]: <10}\n' +
                '{:　<4}'.format('买价') + ': {t[1]: <10}' +  #
                '{:　<4}'.format('最低价') + ': {t[7]: <10}' +
                '{:　<4}'.format('持仓量') + ': {t[13]: <10}' +
                '{:　<4}'.format('申买量二') + ': {t[17]: <10}' +
                '{:　<4}'.format('申买价二') + ': {t[22]: <10}' +
                '{:　<4}'.format('申卖量二') + ': {t[27]: <10}' +
                '{:　<4}'.format('申卖价二') + ': {t[32]: <10}\n' +
                '{:　<4}'.format('卖量') + ': {t[2]: <10}' +  #
                '{:　<4}'.format('昨收价') + ': {t[8]: <10}' +
                '{:　<4}'.format('成交量') + ': {t[14]: <10}' +
                '{:　<4}'.format('申买量三') + ': {t[18]: <10}' +
                '{:　<4}'.format('申买价三') + ': {t[23]: <10}' +
                '{:　<4}'.format('申卖量三') + ': {t[28]: <10}' +
                '{:　<4}'.format('申卖价三') + ': {t[33]: <10}\n' +
                '{:　<4}'.format('卖价') + ': {t[3]: <10}' +  #
                '{:　<4}'.format('开盘价') + ': {t[9]: <10}' +
                '{:　<4}'.format('成交额') + ': {t[15]: <10}' +
                '{:　<4}'.format('申买量四') + ': {t[19]: <10}' +
                '{:　<4}'.format('申买价四') + ': {t[24]: <10}' +
                '{:　<4}'.format('申卖量四') + ': {t[29]: <10}' +
                '{:　<4}'.format('申卖价四') + ': {t[34]: <10}\n' +
                '{:　<4}'.format('最新价') + ': {t[4]: <10}' +  #
                '{:　<4}'.format('涨停价') + ': {t[10]: <10}' +
                '{:　<4}'.format('') + '{: <12}'.format('') +
                '{:　<4}'.format('申买量五') + ': {t[19]: <10}' +
                '{:　<4}'.format('申买价五') + ': {t[24]: <10}' +
                '{:　<4}'.format('申卖量五') + ': {t[29]: <10}' +
                '{:　<4}'.format('申卖价五') + ': {t[34]: <10}\n' +
                '{:　<4}'.format('行权价') + ': {t[5]: <10}' +  #
                '{:　<4}'.format('跌停价') + ': {t[11]: <10}').format(t=text1)
        return 1, res1, '', ''
    # 上交所股票期权: 基础信息
    if lineEdit_code_Text[0] == '1':
        res1 = ('{:　<4}'.format('合约简称') + ': {t[0]: <15}' +  #
                '{:　<4}'.format('买量') + ': {t[6]: <10}' +
                '{:　<4}'.format('最高价') + ': {t[12]: <10}' +
                '{:　<4}'.format('涨幅') + ': {t[18]: <15}' +
                '{:　<4}'.format('申买量一') + ': {t[24]: <5}' +
                '{:　<4}'.format('申买价一') + ': {t[29]: <10}' +
                '{:　<4}'.format('申卖量一') + ': {t[34]: <5}' +
                '{:　<4}'.format('申卖价一') + ': {t[39]: <10}\n' +
                '{:　<4}'.format('标的股票') + ': {t[1]: <13}　　' +  #
                '{:　<4}'.format('买价') + ': {t[7]: <10}' +
                '{:　<4}'.format('最低价') + ': {t[13]: <10}' +
                '{:　<4}'.format('振幅') + ': {t[19]: <15}' +
                '{:　<4}'.format('申买量二') + ': {t[25]: <5}' +
                '{:　<4}'.format('申买价二') + ': {t[30]: <10}' +
                '{:　<4}'.format('申卖量二') + ': {t[35]: <5}' +
                '{:　<4}'.format('申卖价二') + ': {t[40]: <10}\n' +
                '{:　<4}'.format('合约类型') + ': {t[2]: <15}' +  #
                '{:　<4}'.format('卖量') + ': {t[8]: <10}' +
                '{:　<4}'.format('昨收价') + ': {t[14]: <10}' +
                '{:　<4}'.format('持仓量') + ': {t[20]: <15}' +
                '{:　<4}'.format('申买量三') + ': {t[26]: <5}' +
                '{:　<4}'.format('申买价三') + ': {t[31]: <10}' +
                '{:　<4}'.format('申卖量三') + ': {t[36]: <5}' +
                '{:　<4}'.format('申卖价三') + ': {t[41]: <10}\n' +
                '{:　<4}'.format('到期日') + ': {t[3]: <13}　　' +  #
                '{:　<4}'.format('卖价') + ': {t[9]: <10}' +
                '{:　<4}'.format('开盘价') + ': {t[15]: <10}' +
                '{:　<4}'.format('成交量') + ': {t[21]: <15}' +
                '{:　<4}'.format('申买量四') + ': {t[27]: <5}' +
                '{:　<4}'.format('申买价四') + ': {t[32]: <10}' +
                '{:　<4}'.format('申卖量四') + ': {t[37]: <5}' +
                '{:　<4}'.format('申卖价四') + ': {t[42]: <10}\n' +
                '{:　<4}'.format('剩余天数') + ': {t[4]: <13}　　' +  #
                '{:　<4}'.format('最新价') + ': {t[10]: <10}' +
                '{:　<4}'.format('涨停价') + ': {t[16]: <10}' +
                '{:　<4}'.format('成交额') + ': {t[22]: <15}' +
                '{:　<4}'.format('申买量五') + ': {t[28]: <5}' +
                '{:　<4}'.format('申买价五') + ': {t[33]: <10}' +
                '{:　<4}'.format('申卖量五') + ': {t[38]: <5}' +
                '{:　<4}'.format('申卖价五') + ': {t[43]: <10}\n' +
                '{:　<4}'.format('价值状态') + ': {t[5]: <15}' +  #
                '{:　<4}'.format('行权价') + ': {t[11]: <10}' +
                '{:　<4}'.format('跌停价') + ': {t[17]: <10}' +
                '{:　<4}'.format('分红调整') + ': {t[23]: <15}').format(t=text1)
    # 深交所股票期权: 基础信息
    else:
        res1 = ('{:　<4}'.format('合约简称') + ': {t[0]: <18}' +  #
                '{:　<4}'.format('买量') + ': {t[6]: <10}' +
                '{:　<4}'.format('最高价') + ': {t[12]: <10}' +
                '{:　<4}'.format('涨幅') + ': {t[18]: <15}' +
                '{:　<4}'.format('申买量一') + ': {t[24]: <5}' +
                '{:　<4}'.format('申买价一') + ': {t[29]: <10}' +
                '{:　<4}'.format('申卖量一') + ': {t[34]: <5}' +
                '{:　<4}'.format('申卖价一') + ': {t[39]: <10}\n' +
                '{:　<4}'.format('标的股票') + ': {t[1]: <14}　　　　' +  #
                '{:　<4}'.format('买价') + ': {t[7]: <10}' +
                '{:　<4}'.format('最低价') + ': {t[13]: <10}' +
                '{:　<4}'.format('振幅') + ': {t[19]: <15}' +
                '{:　<4}'.format('申买量二') + ': {t[25]: <5}' +
                '{:　<4}'.format('申买价二') + ': {t[30]: <10}' +
                '{:　<4}'.format('申卖量二') + ': {t[35]: <5}' +
                '{:　<4}'.format('申卖价二') + ': {t[40]: <10}\n' +
                '{:　<4}'.format('合约类型') + ': {t[2]: <16}　　' +  #
                '{:　<4}'.format('卖量') + ': {t[8]: <10}' +
                '{:　<4}'.format('昨收价') + ': {t[14]: <10}' +
                '{:　<4}'.format('持仓量') + ': {t[20]: <15}' +
                '{:　<4}'.format('申买量三') + ': {t[26]: <5}' +
                '{:　<4}'.format('申买价三') + ': {t[31]: <10}' +
                '{:　<4}'.format('申卖量三') + ': {t[36]: <5}' +
                '{:　<4}'.format('申卖价三') + ': {t[41]: <10}\n' +
                '{:　<4}'.format('到期日') + ': {t[3]: <14}　　　　' +  #
                '{:　<4}'.format('卖价') + ': {t[9]: <10}' +
                '{:　<4}'.format('开盘价') + ': {t[15]: <10}' +
                '{:　<4}'.format('成交量') + ': {t[21]: <15}' +
                '{:　<4}'.format('申买量四') + ': {t[27]: <5}' +
                '{:　<4}'.format('申买价四') + ': {t[32]: <10}' +
                '{:　<4}'.format('申卖量四') + ': {t[37]: <5}' +
                '{:　<4}'.format('申卖价四') + ': {t[42]: <10}\n' +
                '{:　<4}'.format('剩余天数') + ': {t[4]: <14}　　　　' +  #
                '{:　<4}'.format('最新价') + ': {t[10]: <10}' +
                '{:　<4}'.format('涨停价') + ': {t[16]: <10}' +
                '{:　<4}'.format('成交额') + ': {t[22]: <15}' +
                '{:　<4}'.format('申买量五') + ': {t[28]: <5}' +
                '{:　<4}'.format('申买价五') + ': {t[33]: <10}' +
                '{:　<4}'.format('申卖量五') + ': {t[38]: <5}' +
                '{:　<4}'.format('申卖价五') + ': {t[43]: <10}\n' +
                '{:　<4}'.format('价值状态') + ': {t[5]: <16}　　' +  #
                '{:　<4}'.format('行权价') + ': {t[11]: <10}' +
                '{:　<4}'.format('跌停价') + ': {t[17]: <10}' +
                '{:　<4}'.format('分红调整') + ': {t[23]: <15}').format(t=text1)
    # 上交所, 深交所股票期权: 价值分析, 风险分析
    res2 = ('{:　<5}'.format('最新价') + ': {t[0]: <10}' +
            '{:　<5}'.format('时间价值') + ': {t[1]: <10}' +
            '{:　<5}'.format('内在价值') + ': {t[2]: <10}' +
            '{:　<5}'.format('隐含波动率') + ': {t[3]: <10}\n' +
            '{:　<5}'.format('理论价值') + ': {t[4]: <10}').format(t=text2)
    res3 = ('{: <7}'.format('涨幅') + ': {t[0]: <10}' +
            '{: <7}'.format('振幅') + ': {t[1]: <10}\n' +
            '{: <5}　　'.format('Delta') + ': {t[2]: <10}' +
            '{: <5}　　'.format('Gamma') + ': {t[3]: <10}' +
            '{: <5}　　'.format('Theta') + ': {t[4]: <10}' +
            '{: <5}　　'.format('Vega') + ': {t[5]: <10}\n' +
            '{: <5}'.format('行权概率') + ': {t[6]: <10}').format(t=text3)

    return 1, res1, res2, res3


# k线数据: 计算ma
def ma(list, days):
    emas = list.copy()  # 创造一个和cps一样大小的集合

    for i in range(len(list)):
        if i < days - 1:
            emas[i] = 0
        else:
            ma = 0
            for j in range(i - days, i):
                j += 1
                ma += list[j]
            emas[i] = ma / days
    return emas


def macd(list, fastperiod=12, slowperiod=26, signalperiod=9):
    ema_short = ma(list, fastperiod)
    ema_long = ma(list, slowperiod)
    diff = ema_short - ema_long
    dea = ma(diff, signalperiod)
    macd = 2 * (diff - dea)
    return diff, dea, macd


# k线数据: 返回空的k线数据
def get_empty_k_line():
    df = pd.DataFrame(columns=['d'])
    df['d'] = pd.to_datetime(df['d'])  # 类型转换
    df.set_index('d', inplace=True)  # 设置d为索引
    return df


# k线数据
def get_k_line(lineEdit_code_Text):
    if lineEdit_code_Text[0] == '1' or lineEdit_code_Text[0] == '9':  # 上交所, 深交所股票期权
        # i-时间，p-价格，v-成交，t-持仓，a-均价, d-日期(仅第一项有)
        res = crawler.get_hourline(lineEdit_code_Text)
        if not len(res):
            hour_df = get_empty_k_line()
        else:
            hour_df = pd.DataFrame(res, columns=['i', 'p', 'v', 't', 'a', 'd'])
            hour_df['p'] = pd.to_numeric(hour_df['p'])
            hour_df['v'] = pd.to_numeric(hour_df['v'])
            hour_df['t'] = pd.to_numeric(hour_df['t'])
            hour_df['a'] = pd.to_numeric(hour_df['a'])

        # d-日期, o-开盘价, h-最高价, l-最低价, c-收盘价, v-成交量, ma5/10/20-5/10/20收盘价日均线
        res = crawler.get_dayline('CON', lineEdit_code_Text)

        d_df = pd.DataFrame(res, columns=['d', 'o', 'h', 'l', 'c', 'v'])
        d_df['d'] = pd.to_datetime(d_df['d'])  # 类型转换
        d_df.set_index('d', inplace=True)  # 设置d为索引, 以进行重采样
        d_df['o'] = pd.to_numeric(d_df['o'])
        d_df['h'] = pd.to_numeric(d_df['h'])
        d_df['l'] = pd.to_numeric(d_df['l'])
        d_df['c'] = pd.to_numeric(d_df['c'])
        d_df['v'] = pd.to_numeric(d_df['v'])

        d_df['ma5'] = ma(d_df['c'], 5)
        d_df['ma10'] = ma(d_df['c'], 10)
        d_df['ma20'] = ma(d_df['c'], 20)
        d_df['diff'], d_df['dea'], d_df['macd'] = macd(d_df['c'])

        w_df = pd.DataFrame(columns=['o', 'h', 'l', 'c', 'v'])
        w_df['o'] = d_df['o'].resample('W').first()  # 以周为单位进行重采样
        w_df['h'] = d_df['h'].resample('W').max()
        w_df['l'] = d_df['l'].resample('W').min()
        w_df['c'] = d_df['c'].resample('W').last()
        w_df['v'] = d_df['v'].resample('W').sum()
        w_df = w_df.drop(w_df[w_df.isnull().T.any()].index, axis=0)

        w_df['ma5'] = ma(w_df['c'], 5)
        w_df['ma10'] = ma(w_df['c'], 10)
        w_df['ma20'] = ma(w_df['c'], 20)
        w_df['diff'], w_df['dea'], w_df['macd'] = macd(w_df['c'])

        m_df = pd.DataFrame(columns=['o', 'h', 'l', 'c', 'v'])
        m_df['o'] = w_df['o'].resample('M').first()  # 以月为单位进行重采样
        m_df['h'] = w_df['h'].resample('M').max()
        m_df['l'] = w_df['l'].resample('M').min()
        m_df['c'] = w_df['c'].resample('M').last()
        m_df['v'] = w_df['v'].resample('M').sum()
        m_df = m_df.drop(m_df[m_df.isnull().T.any()].index, axis=0)

        m_df['ma5'] = ma(m_df['c'], 5)
        m_df['ma10'] = ma(m_df['c'], 10)
        m_df['ma20'] = ma(m_df['c'], 20)
        m_df['diff'], m_df['dea'], m_df['macd'] = macd(m_df['c'])

        return hour_df, d_df, w_df, m_df

    else:  # 中金所股票期权 / 商品期权
        res = crawler.get_dayline('P', lineEdit_code_Text)

        # d-日期, o-开盘价, h-最高价, l-最低价, c-收盘价, v-成交量
        d_df = pd.DataFrame(res,
                            columns=['d', 'o', 'h', 'l', 'c', 'v'])
        d_df['d'] = pd.to_datetime(d_df['d'])  # 类型转换
        d_df.set_index('d', inplace=True)  # 设置d为索引, 以进行重采样
        d_df['o'] = pd.to_numeric(d_df['o'])
        d_df['h'] = pd.to_numeric(d_df['h'])
        d_df['l'] = pd.to_numeric(d_df['l'])
        d_df['c'] = pd.to_numeric(d_df['c'])
        d_df['v'] = pd.to_numeric(d_df['v'])

        d_df['ma5'] = ma(d_df['c'], 5)
        d_df['ma10'] = ma(d_df['c'], 10)
        d_df['ma20'] = ma(d_df['c'], 20)
        d_df['diff'], d_df['dea'], d_df['macd'] = macd(d_df['c'])

        w_df = pd.DataFrame(columns=['o', 'h', 'l', 'c', 'v'])
        w_df['o'] = d_df['o'].resample('W').first()  # 以周为单位进行重采样
        w_df['h'] = d_df['h'].resample('W').max()
        w_df['l'] = d_df['l'].resample('W').min()
        w_df['c'] = d_df['c'].resample('W').last()
        w_df['v'] = d_df['v'].resample('W').sum()
        w_df = w_df.drop(w_df[w_df.isnull().T.any()].index, axis=0)

        w_df['ma5'] = ma(w_df['c'], 5)
        w_df['ma10'] = ma(w_df['c'], 10)
        w_df['ma20'] = ma(w_df['c'], 20)
        w_df['diff'], w_df['dea'], w_df['macd'] = macd(w_df['c'])

        m_df = pd.DataFrame(columns=['o', 'h', 'l', 'c', 'v'])
        m_df['o'] = w_df['o'].resample('M').first()  # 以月为单位进行重采样
        m_df['h'] = w_df['h'].resample('M').max()
        m_df['l'] = w_df['l'].resample('M').min()
        m_df['c'] = w_df['c'].resample('M').last()
        m_df['v'] = w_df['v'].resample('M').sum()
        m_df = m_df.drop(m_df[m_df.isnull().T.any()].index, axis=0)

        m_df['ma5'] = ma(m_df['c'], 5)
        m_df['ma10'] = ma(m_df['c'], 10)
        m_df['ma20'] = ma(m_df['c'], 20)
        m_df['diff'], m_df['dea'], m_df['macd'] = macd(m_df['c'])

        return get_empty_k_line(), d_df, w_df, m_df


'''
价值潜力榜
'''


# 价值潜力榜
def get_tableWidget_rank(spinBox_rank_buy_value, spinBox_rank_sell_value, spinBox_rank_v_value,
                         radioButton_buy_isChecked, horizontalSlider_rank_value):
    # 是否应用LSTM模型
    useLSTM = True
    proportion = 1

    res = crawler.get_msg_rank(spinBox_rank_buy_value, spinBox_rank_sell_value, spinBox_rank_v_value)

    # 应用LSTM模型且交易偏好存在短期
    if useLSTM and horizontalSlider_rank_value > 0:
        import LSTM
        VPs = LSTM.get_all_VPs()

        if horizontalSlider_rank_value == 99:
            for i in range(len(res)):
                res[i][-1] = float(res[i][-3]) * proportion * VPs[res[i][2]]
                if '沽' in res[i][1]:
                    res[i][-1] *= -1
        else:
            for i in range(len(res)):
                res[i][-1] = (horizontalSlider_rank_value / 99 * float(res[i][-3]) * proportion * VPs[res[i][2]] +
                              (1 - horizontalSlider_rank_value / 99) * float(res[i][-1]))
                if '沽' in res[i][1]:
                    res[i][-1] *= -1

        if radioButton_buy_isChecked:
            res.sort(key=lambda x: x[-1], reverse=True)  # 按照价值潜力逆序排序
        else:
            res.sort(key=lambda x: x[-1], reverse=False)  # 按照价值潜力正序排序

        # 截取价值潜力在0之前的合约
        end = -1
        for i in range(len(res)):
            if (radioButton_buy_isChecked and res[i][-1] <= 0) or (not radioButton_buy_isChecked and res[i][-1] >= 0):
                end = i
                break

            delta = float(res[i][-3]) * 100
            if delta < 0:
                delta = -delta
            res[i][-3] = format(delta, '.2f') + '%'

            res[i][-1] = format(res[i][-1], '.4f')


        return res[0:end]

    # 不应用LSTM模型
    if radioButton_buy_isChecked:
        res.sort(key=lambda x: float(x[-1]), reverse=True)  # 按照价值潜力逆序排序
    else:
        res.sort(key=lambda x: float(x[-1]), reverse=False)  # 按照价值潜力正序排序

    # 截取价值潜力在0之前的合约
    end = -1
    for i in range(len(res)):
        if res[i][-1][-4:] == '0.00':
            end = i
            break

        delta = float(res[i][-3]) * 100
        if delta < 0:
            delta = -delta
        res[i][-3] = format(delta, '.2f') + '%'

    return res[0:end]

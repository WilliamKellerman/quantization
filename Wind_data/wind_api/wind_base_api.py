import json
from urllib.parse import urlencode, ParseResult

import pandas as pd
import requests


import single_fund_season_report_data as md

MOCK_MODE = True
SESSION_ID = '743b46dbada142519e0f9d0e246b0361'
HOST = '114.80.154.45'


def generate_fund_heavy_stock_url_header():
    # 拼装url
    # url is http://114.80.154.45/FundCoreWeb/WebService?Name=Common.CloudDynamicPicker&wind.sessionid=2d98e3ffb99f42c2a7e8e5ab31af2d14&_r=0.7139373540625608

    path = '/FundCoreWeb/WebService'

    query_args = {
        'Name': 'Common.CloudDynamicPicker',
        'wind.sessionid': SESSION_ID,
        '_r': '0.7139373540625608'
    }
    encoded_args = urlencode(query_args)

    url = ParseResult(scheme='http', netloc=HOST, path=path, params='', query=encoded_args, fragment='').geturl()

    print('url is ' + url)

    return url


def generate_headers():
    # 拼装headers
    headers = {
        # 理论上只要'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 验证发现header里所有参数都可以去掉,
        'Host': HOST,
        'wind.sessionid': SESSION_ID,
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'Accept-Language': 'en-us',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'http://' + HOST,
        # 'Content-Length': '449',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16) AppleWebKit/605.1.15 (KHTML, like Gecko)',
        'Referer': 'http://' + HOST + '/FundResearchWeb/PublicFundF9/index.html?wind.sessionid=' + SESSION_ID,
        'Cookie': 'ASP.NET_SessionId=kgqiwa55vg2o5l550qvir3qn; '
                  'curSearchUserType={%22result%22:[]}; '
                  'isBig5ToGb=undefined; langType=CHS; '
                  'tipsArrayNew=[%22%E6%B1%87%E4%B8%B0%E6%99%8B%E4%BF%A1%22]; '
                  'versionId=206100000'
    }
    return headers


# 单只基金重仓(多季)
def get_one_fund_heavy_stock_hold(fund_code: str, report_date_list: list) -> pd.DataFrame:
    print('单只基金重仓(多季)：fund_code is ' + fund_code)
    single_fund_df = pd.DataFrame
    if MOCK_MODE:
        single_fund_df = md.get_mock_fund_data(report_date_list)
    else:
        # 拼装url，headers
        url = generate_fund_heavy_stock_url_header()
        headers = generate_headers()
        # 拼装data
        cmd = '[{"Name":"Common.CloudDynamicPicker","Paras":[{"Key":"command","Value":" Report name=F9_2.Fund.StocInvePortfolio.HeavHeldStockStock23 windCode=[' + fund_code + '] reportDate=[' + ','.join(report_date_list) + '] industryType=[''] sort=[10=asc,2=desc] showcolumnname=all "},{"Key":"digits","Value":4}],"CacheLevel":1,"Async":false}]'
        data = {'invoke': cmd}
        response = requests.post(url=url, data=data, headers=headers)

        if 200 == response.status_code:
            text = json.loads(response.text)
            if text.get('Result') is not None:
                data = text.get('Result').get('Data')
                single_fund_df = pd.DataFrame(data)
            else:
                print(text)
                raise Exception("Invalid response" + text)
        else:
            print(response.status_code)
            raise Exception("Invalid response" + response.status_code)

    # 股票代码 "StockCode": "002271.SZ",
    # 股票名称  "StockName": "东方雨虹",
    # 持仓市值(元)  "MarketValue": 2202471541.2,
    # 持仓数量  "Share": 57585349,
    # 占股票市值比(%)  "StockMarketValuePer": 7.9629,
    # 占基金净值比(%)  "FundNetPer": 7.2357,
    # 占流通股本比(%)  "TradeableSharePer": 3.4242,
    # 相对上期增减(%) -> 持仓数量变动比(%)  "PreSub": 159.0662,
    # 区间涨跌幅  "PerChange": 7.9777,
    # 持仓数量变动  "PreSubVol": 35357309,
    # 报告期  "RptDate": "2020-12-31",
    # 所属行业  "IndustryName": "建筑材料"
    single_fund_df.rename(columns={'StockCode': '股票代码',
                                   'StockName': '股票名称',
                                   'MarketValue': '持仓市值(亿)',
                                   'Share': '持仓数量',
                                   'StockMarketValuePer': '占股票市值比(%)',
                                   'FundNetPer': '占基金净值比(%)',
                                   'TradeableSharePer': '占流通股本比(%)',
                                   'PreSub': '持仓数量变动比(%)',
                                   'PerChange': '股价涨跌幅(%)',
                                   'PreSubVol': '持仓数量变动',
                                   'RptDate': '报告期',
                                   'IndustryName': '所属行业'
                                   }, inplace=True)

    return single_fund_df


# 单只基金重仓(单季)
def get_one_fund_one_season_heavy_stock_hold(fund_code: str, report_date: str) -> list:
    report_date_list = get_one_fund_heavy_stock_hold(fund_code=fund_code, report_date_list=[report_date])
    return report_date_list



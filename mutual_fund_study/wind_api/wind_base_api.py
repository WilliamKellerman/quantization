import json
from urllib.parse import urlencode, ParseResult
from customize_exception import CustomizeException
import pandas as pd
import requests
import single_fund_season_report_data as md


class WindApi:
    def __init__(self, fund_code: str, report_date_list: list):
        self.fund_code = fund_code
        self.report_date_list = report_date_list
        self.__MOCK_MODE = True
        self.__SESSION_ID = '834c45fe1ad44214af5f1b56d36deac3'
        self.__HOST = '114.80.154.45'

    def __generate_fund_heavy_stock_url(self):
        # 拼装url
        # url is http://114.80.154.45/FundCoreWeb/WebService?Name=Common.CloudDynamicPicker&wind.sessionid=2d98e3ffb99f42c2a7e8e5ab31af2d14&_r=0.7139373540625608

        path = '/FundCoreWeb/WebService'

        query_args = {
            'Name': 'Common.CloudDynamicPicker',
            'wind.sessionid': self.__SESSION_ID,
            '_r': '0.7139373540625608'
        }
        encoded_args = urlencode(query_args)

        url = ParseResult(scheme='http', netloc=self.__HOST, path=path, params='', query=encoded_args, fragment='').geturl()

        print('url is ' + url)

        return url

    def __generate_headers(self):
        # 拼装headers
        headers = {
            # 理论上只要'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 验证发现header里所有参数都可以去掉,
            'Host': self.__HOST,
            'wind.sessionid': self.__SESSION_ID,
            'Accept': 'application/json, text/plain, */*',
            'Connection': 'keep-alive',
            'Accept-Language': 'en-us',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'http://' + self.__HOST,
            # 'Content-Length': '449',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16) AppleWebKit/605.1.15 (KHTML, like Gecko)',
            'Referer': 'http://' + self.__HOST + '/FundResearchWeb/PublicFundF9/index.html?wind.sessionid=' + self.__SESSION_ID,
            'Cookie': 'ASP.NET_SessionId=kgqiwa55vg2o5l550qvir3qn; '
                      'curSearchUserType={%22result%22:[]}; '
                      'isBig5ToGb=undefined; langType=CHS; '
                      'tipsArrayNew=[%22%E6%B1%87%E4%B8%B0%E6%99%8B%E4%BF%A1%22]; '
                      'versionId=206100000'
        }
        return headers

    def get_one_fund_heavy_stock_hold(self) -> pd.DataFrame:
        print('单只基金重仓(多季)：fund_code is ' + self.fund_code)
        single_fund_df = pd.DataFrame
        if self.__MOCK_MODE:
            single_fund_df = md.get_mock_fund_data(self.report_date_list)
        else:
            url = self.__generate_fund_heavy_stock_url()
            headers = self.__generate_headers()
            # 拼装data
            cmd = '[{"Name":"Common.CloudDynamicPicker","Paras":[{"Key":"command","Value":" Report name=F9_2.Fund.StocInvePortfolio.HeavHeldStockStock23 windCode=[' + \
                  self.fund_code + '] reportDate=[' + ','.join(self.report_date_list) + \
                  '] industryType=[''] sort=[10=asc,2=desc] showcolumnname=all "},{"Key":"digits","Value":4}],"CacheLevel":1,"Async":false}]'
            data = {'invoke': cmd}
            response = requests.post(url=url, data=data, headers=headers)

            if 200 == response.status_code:
                text = json.loads(response.text)
                if text.get('Result') is not None:
                    data = text.get('Result').get('Data')
                    single_fund_df = pd.DataFrame(data)
                else:
                    print(text)
                    raise CustomizeException(None, "Invalid response: Result is None")
            else:
                raise CustomizeException(response.status_code, 'Invalid response, status_code=')

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
    def get_one_fund_one_season_heavy_stock_hold(self) -> list:
        report_date_list = self.get_one_fund_heavy_stock_hold()
        return report_date_list

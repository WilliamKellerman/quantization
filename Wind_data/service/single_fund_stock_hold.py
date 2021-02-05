import date_utility
import wind_base_api
import pandas as pd


# 单基金多季度持仓数量汇总
def get_one_fund_all_season_stock_hold_vol(fund_code: str, start_date: str, end_date: str) -> pd.DataFrame:
    report_date_list = date_utility.generate_season_date_list(start_date=start_date, end_date=end_date)

    all_season_long_df = wind_base_api.get_one_fund_heavy_stock_hold(fund_code=fund_code,
                                                                     report_date_list=report_date_list)

    all_season_df = pd.DataFrame
    for report_date in report_date_list:
        report_date_formatted = date_utility.date_format_str_to_str(date_in=report_date,
                                                                    format_in="%Y%m%d",
                                                                    format_out="%Y-%m-%d")

        # 根据报告期切片 single_season_df
        single_season_df = all_season_long_df[all_season_long_df['报告期'] == report_date_formatted]
        single_season_df = single_season_df[['股票代码', '股票名称', '持仓数量']]
        if single_season_df.empty:
            continue
        else:
            single_season_df.rename(columns={'持仓数量': report_date}, inplace=True)
            if all_season_df.empty:
                all_season_df = single_season_df
            else:
                all_season_df = pd.merge(left=all_season_df, right=single_season_df, how='outer', on=('股票代码', '股票名称'))
    return all_season_df
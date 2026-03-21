# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from jqdata import *

"""
策略说明
1. 当日14:30同时满足以下9个条件才买入：
   - 条件1：截至14:30涨幅在3%-5%
   - 条件2：近20日有过涨停强势记忆
   - 条件3：当日量比大于1，并且近几日温和放量
   - 条件4：市值低于200亿
   - 条件5：换手率5%-10%之间（14:30用成交额/总市值近似）
   - 条件6：14:30价格在VWAP上方，且分时大部分时间运行在VWAP上方
   - 条件7：14:30价格站上MA5和MA10
   - 条件8：14:30振幅 > 5%
   - 条件9：14:30收盘位置偏上，尽量接近日内上沿（这里定义为 close_pos >= 0.7）

2. 买入：
   - 当日14:30买入

3. 卖出：
   - 下一交易日10:00卖出

4. 输出：
   - 总体收益统计
   - 按上证指数14:30涨跌幅环境分组统计
"""


def initialize(context):
    set_benchmark('000300.XSHG')
    set_option('use_real_price', True)
    set_option('order_volume_ratio', 1)

    set_order_cost(OrderCost(
        open_tax=0,
        close_tax=0.001,
        open_commission=0.0003,
        close_commission=0.0003,
        close_today_commission=0,
        min_commission=5
    ), type='stock')

    g.position_info = {}
    g.trade_records = []

    run_daily(buy_signal_1430, time='14:30')
    run_daily(sell_next_day_1000, time='10:00')
    run_daily(report_result, time='after_close')


def get_sh_index_bucket(current_date):
    index_code = '000001.XSHG'

    minute_df = get_price(
        index_code,
        start_date=current_date + ' 09:30:00',
        end_date=current_date + ' 14:30:00',
        frequency='1m',
        fields=['close'],
        fq='pre',
        panel=False
    )
    daily_df = get_price(
        index_code,
        end_date=current_date,
        count=2,
        frequency='daily',
        fields=['close'],
        fq='pre',
        panel=False
    )

    if minute_df is None or len(minute_df) == 0 or daily_df is None or len(daily_df) < 2:
        return None, np.nan

    prev_close = daily_df['close'].iloc[-2]
    cur_1430 = minute_df['close'].iloc[-1]
    idx_ret = cur_1430 / prev_close - 1

    if 0 <= idx_ret < 0.005:
        bucket = '涨幅<0.5%'
    elif 0.005 <= idx_ret < 0.01:
        bucket = '涨幅0.5%-1%'
    elif idx_ret >= 0.01:
        bucket = '涨幅>1%'
    elif -0.005 < idx_ret < 0:
        bucket = '跌幅<0.5%'
    elif -0.01 < idx_ret <= -0.005:
        bucket = '跌幅0.5%-1%'
    else:
        bucket = '跌幅>1%'

    return bucket, idx_ret


def buy_signal_1430(context):
    current_date = context.current_dt.strftime('%Y-%m-%d')
    current_data = get_current_data()

    index_bucket, index_ret_1430 = get_sh_index_bucket(current_date)

    stocks = list(get_all_securities(types=['stock'], date=current_date).index)

    stock_list = []
    for s in stocks:
        if current_data[s].paused:
            continue
        if current_data[s].is_st:
            continue
        if 'ST' in current_data[s].name or '*' in current_data[s].name:
            continue
        if (context.current_dt.date() - get_security_info(s).start_date).days < 60:
            continue
        stock_list.append(s)

    if len(stock_list) == 0:
        return

    q = query(
        valuation.code,
        valuation.market_cap
    ).filter(
        valuation.code.in_(stock_list),
        valuation.market_cap < 200
    )

    funda = get_fundamentals(q, date=current_date)
    if funda is None or len(funda) == 0:
        return

    cap_map = dict(zip(funda['code'], funda['market_cap']))
    candidate_stocks = list(funda['code'])

    daily_df = get_price(
        candidate_stocks,
        end_date=current_date,
        count=30,
        frequency='daily',
        fields=['close', 'high', 'low', 'volume', 'money', 'high_limit'],
        fq='pre',
        panel=False
    )
    if daily_df is None or len(daily_df) == 0:
        return

    min_df = get_price(
        candidate_stocks,
        start_date=current_date + ' 09:30:00',
        end_date=current_date + ' 14:30:00',
        frequency='1m',
        fields=['close', 'high', 'low', 'volume', 'money'],
        fq='pre',
        panel=False
    )
    if min_df is None or len(min_df) == 0:
        return

    prev_trade_days = get_trade_days(end_date=context.previous_date, count=5)
    hist_vol_map = {}

    for d in prev_trade_days:
        d_str = str(d)
        hist_min_df = get_price(
            candidate_stocks,
            start_date=d_str + ' 09:30:00',
            end_date=d_str + ' 14:30:00',
            frequency='1m',
            fields=['volume'],
            fq='pre',
            panel=False
        )
        if hist_min_df is None or len(hist_min_df) == 0:
            continue

        tmp = hist_min_df.groupby('code')['volume'].sum()
        for code, vol in tmp.items():
            hist_vol_map.setdefault(code, []).append(vol)

    buy_list = []

    for code in candidate_stocks:
        dfg = daily_df[daily_df['code'] == code].sort_values('time')
        mfg = min_df[min_df['code'] == code].sort_values('time')

        if len(dfg) < 21 or len(mfg) == 0:
            continue

        prev_close = dfg['close'].iloc[-2]
        price_1430 = mfg['close'].iloc[-1]
        high_1430 = mfg['high'].max()
        low_1430 = mfg['low'].min()
        vol_1430 = mfg['volume'].sum()
        amt_1430 = mfg['money'].sum()

        ret_1430 = price_1430 / prev_close - 1
        cond1 = 0.03 <= ret_1430 <= 0.05

        recent20 = dfg.tail(20).copy()
        recent_ret = recent20['close'].pct_change()
        limit_memory = (recent20['close'] >= recent20['high_limit'] * 0.995).any()
        strong_memory = (recent_ret >= 0.08).any()
        cond2 = bool(limit_memory or strong_memory)

        hist_avg_vol = np.mean(hist_vol_map.get(code, [])) if len(hist_vol_map.get(code, [])) > 0 else np.nan
        vol_ratio = vol_1430 / hist_avg_vol if pd.notna(hist_avg_vol) and hist_avg_vol > 0 else np.nan

        vol_series = dfg['volume']
        recent3 = vol_series.iloc[-4:-1].mean()
        prev5 = vol_series.iloc[-9:-4].mean() if len(vol_series) >= 9 else np.nan
        mild_expand = pd.notna(prev5) and recent3 > prev5 and recent3 < prev5 * 2
        cond3 = pd.notna(vol_ratio) and vol_ratio > 1 and mild_expand

        market_cap = cap_map.get(code, np.nan)
        cond4 = pd.notna(market_cap) and market_cap < 200

        turnover_proxy = amt_1430 / (market_cap * 1e8) if pd.notna(market_cap) and market_cap > 0 else np.nan
        cond5 = pd.notna(turnover_proxy) and 0.05 <= turnover_proxy <= 0.10

        cum_amt = mfg['money'].cumsum()
        cum_vol = mfg['volume'].cumsum().replace(0, np.nan)
        vwap_series = cum_amt / cum_vol
        vwap_1430 = vwap_series.iloc[-1]
        above_vwap_ratio = (mfg['close'] > vwap_series).mean()
        cond6 = (price_1430 > vwap_1430) and (above_vwap_ratio > 0.6)

        ma5 = dfg['close'].tail(5).mean()
        ma10 = dfg['close'].tail(10).mean()
        cond7 = (price_1430 > ma5) and (price_1430 > ma10)

        amp_1430 = high_1430 / low_1430 - 1 if low_1430 > 0 else np.nan
        cond8 = pd.notna(amp_1430) and amp_1430 > 0.05

        close_pos = (price_1430 - low_1430) / (high_1430 - low_1430) if high_1430 > low_1430 else 0
        cond9 = close_pos >= 0.7

        if cond1 and cond2 and cond3 and cond4 and cond5 and cond6 and cond7 and cond8 and cond9:
            buy_list.append(code)

    if len(buy_list) == 0:
        log.info('14:30 无符合条件股票 | 上证14:30涨跌幅: {:.2%} | 分组: {}'.format(index_ret_1430, index_bucket))
        return

    log.info('14:30 买入候选数: {} | 上证14:30涨跌幅: {:.2%} | 分组: {}'.format(
        len(buy_list), index_ret_1430, index_bucket
    ))
    log.info('买入列表: {}'.format(buy_list))

    available_cash = context.portfolio.cash
    if available_cash <= 0:
        return

    cash_per_stock = available_cash / len(buy_list)

    for stock in buy_list:
        order_value(stock, cash_per_stock)
        buy_price = current_data[stock].last_price
        g.position_info[stock] = {
            'buy_date': context.current_dt.date(),
            'buy_price': buy_price,
            'index_bucket': index_bucket,
            'index_ret_1430': index_ret_1430
        }


def sell_next_day_1000(context):
    if len(context.portfolio.positions) == 0:
        return

    sell_list = []

    for stock in list(context.portfolio.positions.keys()):
        if stock not in g.position_info:
            continue

        info = g.position_info[stock]
        buy_date = info['buy_date']

        hold_days = get_trade_days(start_date=buy_date, end_date=context.current_dt.date())
        if len(hold_days) < 2:
            continue

        cur_price = get_current_data()[stock].last_price
        buy_price = info['buy_price']
        ret = cur_price / buy_price - 1 if buy_price > 0 else np.nan

        g.trade_records.append({
            'stock': stock,
            'buy_date': buy_date,
            'sell_date': context.current_dt.date(),
            'buy_price': buy_price,
            'sell_price': cur_price,
            'ret': ret,
            'index_bucket': info['index_bucket'],
            'index_ret_1430': info['index_ret_1430']
        })

        sell_list.append(stock)

    for stock in sell_list:
        order_target_value(stock, 0)
        g.position_info.pop(stock, None)


def report_group_stats(df, group_name):
    ret = df['ret'].dropna()
    if len(ret) == 0:
        return

    avg_ret = ret.mean()
    median_ret = ret.median()
    win_rate = (ret > 0).mean()

    win_ret = ret[ret > 0]
    loss_ret = ret[ret <= 0]

    avg_win = win_ret.mean() if len(win_ret) > 0 else np.nan
    avg_loss = loss_ret.mean() if len(loss_ret) > 0 else np.nan
    profit_loss = avg_win / abs(avg_loss) if pd.notna(avg_win) and pd.notna(avg_loss) and avg_loss != 0 else np.nan

    log.info('------ {} ------'.format(group_name))
    log.info('样本数: {}'.format(len(ret)))
    log.info('平均收益: {:.2%}'.format(avg_ret))
    log.info('中位数收益: {:.2%}'.format(median_ret))
    log.info('胜率: {:.2%}'.format(win_rate))
    if pd.notna(avg_win):
        log.info('平均盈利: {:.2%}'.format(avg_win))
    if pd.notna(avg_loss):
        log.info('平均亏损: {:.2%}'.format(avg_loss))
    if pd.notna(profit_loss):
        log.info('盈亏比: {:.2f}'.format(profit_loss))


def report_result(context):
    if len(g.trade_records) == 0:
        return

    df = pd.DataFrame(g.trade_records)
    if len(df) == 0:
        return

    log.info('====== 总体统计结果 ======')
    report_group_stats(df, '总体')

    bucket_order = [
        '涨幅<0.5%',
        '涨幅0.5%-1%',
        '涨幅>1%',
        '跌幅<0.5%',
        '跌幅0.5%-1%',
        '跌幅>1%'
    ]

    log.info('====== 按上证指数14:30涨跌幅分组统计 ======')
    for bucket in bucket_order:
        sub = df[df['index_bucket'] == bucket].copy()
        if len(sub) > 0:
            report_group_stats(sub, bucket)

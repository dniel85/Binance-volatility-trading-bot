from tradingview_ta import TA_Handler, Interval, Exchange
import os
import time

INTERVAL = Interval.INTERVAL_1_MINUTE  # Timeframe for analysis

EXCHANGE = 'BINANCE'
SCREENER = 'CRYPTO'
SYMBOL = 'BTCUSDT'
THRESHOLD = 7  # 7 of 15 MA's indicating sell
TIME_TO_WAIT = 1  # Minutes to wait between analysis
FULL_LOG = False  # List analysis result to console


def analyze():
    analysis = {}
    handler = {}

    handler = TA_Handler(
        symbol=SYMBOL,
        exchange=EXCHANGE,
        screener=SCREENER,
        interval=INTERVAL,
        timeout=10)

    try:
        analysis = handler.get_analysis()
    except Exception as e:
        print("pausebotmod:")
        print("Exception:")
        print(e)

    with open('signals/paused.exc', 'r')  as previous_status:
        previous_status.read()
        print(previous_status)

    ma_sell = analysis.moving_averages['SELL']
    if ma_sell > THRESHOLD and ma_sell < 13:
        status = 'DOWNTREND'
        print(
            f'pausebotmod: Market is in a DOWNTREND, bot paused from buying {ma_sell}/{THRESHOLD} Waiting {TIME_TO_WAIT} minutes for next market checkup')
    if ma_sell >= 13:
        print(
            f'pausebotmod: Market is BEARISH, bot paused from buying {ma_sell}/{THRESHOLD} Waiting {TIME_TO_WAIT} minutes for next market checkup')
        status = 'BEARISH'
    if ma_sell <= THRESHOLD and ma_sell >= 5:
        print(
            f'pausebotmod: Market is in an UPTREND, bot is running {ma_sell}/{THRESHOLD} Waiting {TIME_TO_WAIT} minutes for next market checkup ')
        status = 'UPTREND'
    if ma_sell <= 4:
        print(
            f'pausebotmod: Market is BULLISH, bot is running {ma_sell}/{THRESHOLD} Waiting {TIME_TO_WAIT} minutes for next market checkup ')
        status = 'BULLISH'

    return status


# if __name__ == '__main__':
def do_work():
    while True:
        # print(f'pausebotmod: Fetching market state')
        status = analyze()
        with open('signals/paused.exc', 'w') as f:
            f.write(status)

        if status == 'DOWNTREND' or status == 'BEARISH':
            # print(f'pausebotmod: Waiting {TIME_TO_WAIT} minutes for next market checkup')    
            time.sleep((TIME_TO_WAIT * 60))

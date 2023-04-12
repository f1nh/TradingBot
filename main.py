from strategy import *

try:

    telegram_send.send(messages=['Connected...'])
    symbols = ['BTCUSDT',
            'BUSDUSDT',
            'ETHUSDT',
            'TWTUSDT',
            'DOGEUSDT',
            'FTTUSDT',
            'BNBUSDT',
            'AXSUSDT',
            'XRPUSDT',
            'MATICUSDT',
            'SOLUSDT',
            'DYDXUSDT',
            'CHZUSDT',
            'TRXUSDT',
            'SFPUSDT',
            'ADAUSDT',
            'LINKUSDT',
            'SHIBUSDT',
            'MASKUSDT',
            'SANDUSDT', 
            'UNIUSDT',
            'LTCUSDT',
            'ATOMUSDT',
            'APTUSDT',
            'NEARUSDT',
            'HFTUSDT',
            'DOTUSDT',
            'CVXUSDT',
            'EURUSDT',
            'C98USDT',
            'APEUSDT',
            'ALGOUSDT',
            'GMTUSDT',
            'AVAXUSDT',
            'SUSHIUSDT',
            'WAVESUSDT',
            'OPUSDT',
            'GALAUSDT',
            'DODOUSDT',
            'PEOPLEUSDT',
            'AAVEUSDT',
            'FILUSDT',
            'ETCUSDT',
            'FTMUSDT',
            'TORNUSDT',
            'SRMUSDT',
            'MANAUSDT',
            'ANKRUSDT',
            'NEOUSDT',
            'ICPUSDT',
            'PERPUSDT',
            'GMXUSDT',
            'TVKUSDT',
            'BAKEUSDT',
            'SXPUSDT',
            'ENSUSDT',
            'LUNAUSDT']

    schedule.every(86400).seconds.do(counter)

    while True:

        for symbol in symbols:

            client = Client(api_key, api_secret, {"verify": True, "timeout": 50000})

            strategy(symbol, client)

            time.sleep(3)

except Exception as e:

    telegram_send.send(messages=[f'Main Bot Error:\n{str(e)}'])
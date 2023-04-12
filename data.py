from subprocess import TimeoutExpired
from modules import *
from config import *

def get_data(symbol, client, interval=interval, past=past):
    
    frame = pd.DataFrame(client.get_historical_klines(symbol,
     interval,past+' min ago UTC'))
    frame = frame.iloc[:, :6]
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    frame = frame.set_index('Time')
    frame.index = pd.to_datetime(frame.index, unit = 'ms')
    frame = frame.astype(float)
    
    return frame

async def main():
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client, user_timeout=60)
    # Start any Sockets here
    ts = bm.trades_socket('BTCUSDT')
    # Then start receiving messages
    async with ts as tscm:
        while True:
            res = await tscm.recv()
            print(res)
            
    await client.close_connection()

def Calculation(df):
    
    # df['rsi'] = tl.RSI(np.array(df['Close']), timeperiod=14)
    # df['ema41'] = tl.EMA(np.array(df['Close']), timeperiod=41)
    # df['ema99'] = tl.EMA(np.array(df['Close']), timeperiod=99)
    df['ema200'] = tl.EMA(np.array(df['Close']), timeperiod=200)
    df['engulf'] = tl.CDLENGULFING(np.array(df['Open']), np.array(df['High']), np.array(df['Low']), np.array(df['Close']))
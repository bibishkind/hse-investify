# trading_view.py
import requests

INFO_URL_PREFIX = "https://scanner.tradingview.com/symbol?fields=Recommend.Other,Recommend.All,Recommend.MA,RSI,RSI[1],Stoch.K,Stoch.D,Stoch.K[1],Stoch.D[1],CCI20,CCI20[1],ADX,ADX+DI,ADX-DI,ADX+DI[1],ADX-DI[1],AO,AO[1],AO[2],Mom,Mom[1],MACD.macd,MACD.signal,Rec.Stoch.RSI,Stoch.RSI.K,Rec.WR,W.R,Rec.BBPower,BBPower,Rec.UO,UO,EMA10,close,SMA10,EMA20,SMA20,EMA30,SMA30,EMA50,SMA50,EMA100,SMA100,EMA200,SMA200,Rec.Ichimoku,Ichimoku.BLine,Rec.VWMA,VWMA,Rec.HullMA9,HullMA9,Pivot.M.Classic.S3,Pivot.M.Classic.S2,Pivot.M.Classic.S1,Pivot.M.Classic.Middle,Pivot.M.Classic.R1,Pivot.M.Classic.R2,Pivot.M.Classic.R3,Pivot.M.Fibonacci.S3,Pivot.M.Fibonacci.S2,Pivot.M.Fibonacci.S1,Pivot.M.Fibonacci.Middle,Pivot.M.Fibonacci.R1,Pivot.M.Fibonacci.R2,Pivot.M.Fibonacci.R3,Pivot.M.Camarilla.S3,Pivot.M.Camarilla.S2,Pivot.M.Camarilla.S1,Pivot.M.Camarilla.Middle,Pivot.M.Camarilla.R1,Pivot.M.Camarilla.R2,Pivot.M.Camarilla.R3,Pivot.M.Woodie.S3,Pivot.M.Woodie.S2,Pivot.M.Woodie.S1,Pivot.M.Woodie.Middle,Pivot.M.Woodie.R1,Pivot.M.Woodie.R2,Pivot.M.Woodie.R3,Pivot.M.Demark.S1,Pivot.M.Demark.Middle,Pivot.M.Demark.R1&no_404=true&symbol="
SEARCH_URL_PREFIX = "https://symbol-search.tradingview.com/symbol_search/v3/?text="

AVAILABLE_INDICATORS = [
    "Индекс относительной силы (14)",
    "Стохастик %K (14, 3, 3)",
    "Моментум (Momentum)",
    "Уровень MACD (12, 26)",
    "Быстрый стохастик RSI (3, 3, 14, 14)",
    "Окончательный осциллятор (7, 14, 28)",
    "Экспоненциальное скользящее среднее (10)",
    "Экспоненциальное скользящее среднее (20)",
    "Экспоненциальное скользящее среднее(30)",
    "Экспоненциальное скользящее среднее (50)",
    "Экспоненциальное скользящее среднее (100)",
    "Экспоненциальное скользящее среднее(200)",
]

def get_info(ticker):
    json = requests.get(get_info_url(ticker)).json()
    return {
        "Индекс относительной силы (14)": round(json["RSI"], 2),
        "Стохастик %K (14, 3, 3)": round(json["Stoch.K"], 2),
        "Моментум (Momentum)": round(json["Mom"], 2),
        "Уровень MACD (12, 26)": round(json["MACD.macd"], 2),
        "Быстрый стохастик RSI (3, 3, 14, 14)": round(json["Stoch.RSI.K"], 2),
        "Окончательный осциллятор (7, 14, 28)": round(json["UO"], 2),
        "Экспоненциальное скользящее среднее (10)": round(json["EMA10"], 2),
        "Экспоненциальное скользящее среднее (20)": round(json["EMA20"], 2),
        "Экспоненциальное скользящее среднее(30)": round(json["EMA30"], 2),
        "Экспоненциальное скользящее среднее (50)": round(json["EMA10"], 2),
        "Экспоненциальное скользящее среднее (100)": round(json["EMA20"], 2),
        "Экспоненциальное скользящее среднее(200)": round(json["EMA30"], 2),
    }

def get_info_url(ticker):
    json = requests.get(SEARCH_URL_PREFIX + ticker).json()
    symbol = json["symbols"][0]
    return INFO_URL_PREFIX + symbol["exchange"] + ":" + symbol["symbol"]

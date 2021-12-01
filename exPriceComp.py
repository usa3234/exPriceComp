import pybithumb
import pyupbit
import math
from binance.client import Client

from bs4 import BeautifulSoup
import urllib.request as req
import re
from time import sleep
import threading
import time
#from bithumAPI.pybithumLocal import Bithumb as bithumbLocal
#import bithumAPI.pybithumCore   
from bithumAPI import pybithumLocal as bithumbLocal
from KAKAOAPI import kakao as kakao

import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests

DIFFER_LIMIT_PERCENT = 10
DIFFER_PRICE = 500000

THREAD_TIME = 3600 #1시간

## 바이낸스
def binanace_get_ticker():
    binanceAccess = "xxx"
    binanceSecret = "xxx"
    binance = Client(binanceAccess, binanceSecret)
    allBinanceCoinList = binance.get_all_tickers()
    #print(binance.get_asset_balance(asset='USDT'))
    
    return allBinanceCoinList

## 업비트
def upbit_all_get_wallet_status(upbitAccess, upbitSecret): 

    payload = {
        'access_key': upbitAccess,
        'nonce': str(uuid.uuid4()),
    }

    jwt_token = jwt.encode(payload, upbitSecret)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.get("https://api.upbit.com" + "/v1/status/wallet", headers=headers)   

    return res.json()

## 빗썸
def bithumb_get_ticker():
    bithumbAccess = "xxx"
    bithumbSecret = "xxx"
    
    bithumb = pybithumb.Bithumb(bithumbAccess, bithumbSecret)

    return bithumb.get_tickers(payment_currency="KRW")

def getUpbitAndBinanceDiff():
    coinNmList = [] 
    for i in range(len(allBinanceCoinList)):
        binanceCoinNm = allBinanceCoinList[i]['symbol']
        #for j in range(len(allUpbitCoinList)):
        for key in allUpbitCoinList:            
            upbitPrice = allUpbitCoinList[key]
            upbitCoinNm = key.replace('KRW-', '') + "USDT"

            if(binanceCoinNm == upbitCoinNm):     
               binanceKRW = float(USDKRW * float(allBinanceCoinList[i]['price']))
               
               #바이낸스에 내돈 원화로 계산
               binanceOwnKRW = float(binance_bal['free']) * USDKRW #KRW 환율계산
               coinCnt = float(binance_bal['free']) / float(allBinanceCoinList[i]['price'])
               upbitTransKRW = float(upbitPrice * coinCnt)

               dfferPercent = 100 - int(abs(binanceKRW / upbitPrice) * 100)

               #if(upbitTransKRW >= DIFFER_PRICE):
               if(dfferPercent >= 10):
               #if(dfferPercent <= DIFFER_LIMIT_PERCENT):
                    coinNmList.append(key)
    return coinNmList


##바이낸스 업비트
def differUpbitAndBinance():   
    msg = "" 
    for i in range(len(allBinanceCoinList)):
        binanceCoinNm = allBinanceCoinList[i]['symbol']
        #for j in range(len(allUpbitCoinList)):
        for key in allUpbitCoinList:            
            upbitPrice = allUpbitCoinList[key]
            upbitCoinNm = key.replace('KRW-', '') + "USDT"

            if(binanceCoinNm == upbitCoinNm):     
               binanceKRW = float(USDKRW * float(allBinanceCoinList[i]['price']))
               
               #바이낸스에 내돈 원화로 계산
               binanceOwnKRW = float(binance_bal['free']) * USDKRW #KRW 환율계산
               coinCnt = float(binance_bal['free']) / float(allBinanceCoinList[i]['price'])
               upbitTransKRW = float(upbitPrice * coinCnt)

               dfferPercent = 100 - int(abs(binanceKRW / upbitPrice) * 100)

               #if(upbitTransKRW >= DIFFER_PRICE):
               if(dfferPercent >= DIFFER_LIMIT_PERCENT):
               #if(dfferPercent <= DIFFER_LIMIT_PERCENT):
                    print(key)                    
                    print(dfferPercent, "차이퍼센트")
                    print(upbitPrice, "업비트")
                    print(binanceKRW, "바이낸스")
                    print(coinCnt, "코인개수")
                    print(binanceOwnKRW, "잔고환율계산금액")
                    print(upbitTransKRW, "현재원화가격")
                    print("")
                    msg += key + "(업비트)" + "\n" + "퍼센트차이 : " + str(dfferPercent) + "\n" + "코인개수 : " + str(coinCnt) + "\n" + "바이낸스원화잔고 : " + str(binanceOwnKRW) + "\n" + "환산원화가격 : " + str(upbitTransKRW) + "\n"
    #kakao.sendMsgMe(msg)
                    

##바이낸스 빗썸
def differBithumbAndBinance():
    msg = ""
    #빗썸 API로컬
    bithumbL = bithumbLocal.Bithumb(bithumbAccess,bithumbSecret)   
    allBithumbStatus =  bithumbL.get_assets_status("ALL")

    for i in range(len(allBinanceCoinList)):
        binanceCoinNm = allBinanceCoinList[i]['symbol']    
        for coinNm in allBithumbCoinList:  
            bithumbPrice = float(allBithumbCoinList[coinNm]['closing_price'])
            bithumbCoinNm = coinNm + "USDT"

            if(binanceCoinNm == bithumbCoinNm):     
               binanceKRW = float(USDKRW * float(allBinanceCoinList[i]['price']))

               #바이낸스에 내돈 원화로 계산
               binanceOwnKRW = float(binance_bal['free']) * USDKRW #KRW 환율계산
               coinCnt = float(binance_bal['free']) / float(allBinanceCoinList[i]['price'])
               bithumbTransKRW = float(bithumbPrice * coinCnt)

               dfferPercent = 100 - int(abs(binanceKRW / bithumbPrice) * 100)

               #if(bithumbTransKRW >= DIFFER_PRICE):
               if(dfferPercent >= DIFFER_LIMIT_PERCENT):
               #if(dfferPercent <= DIFFER_LIMIT_PERCENT):
                    print(coinNm)                    
                    print(dfferPercent, "차이퍼센트")
                    print(bithumbPrice, "빗썸")
                    print(binanceKRW, "바이낸스")
                    print(coinCnt, "코인개수")
                    print(binanceOwnKRW, "잔고환율계산금액")
                    print(bithumbTransKRW, "현재원화가격")
                    print(allBithumbStatus[coinNm]['deposit_status'], "입금가능")                    
                    print(allBithumbStatus[coinNm]['withdrawal_status'], "출급가능")
                    print("")
                    msg += coinNm + "(빗썸)" + "\n" + "퍼센트차이 : " + str(dfferPercent) + "\n" + "코인개수 : " + str(coinCnt) + "\n" + "바이낸스원화잔고 : " + str(binanceOwnKRW) + "\n" + "환산원화가격 : " + str(bithumbTransKRW) + "\n" + "입금가능 : " + str(allBithumbStatus[coinNm]['deposit_status']) + "\n" + "출급가능 : " + str(allBithumbStatus[coinNm]['withdrawal_status']) + "\n"
    #kakao.sendMsgMe(msg)

## 환율정보 가져오기
def get_exchange_USD():
    # HTML 가져오기
    url = "http://finance.naver.com/marketindex/"
    res = req.urlopen(url)

    # HTML 분석하기
    soup = BeautifulSoup(res, "html.parser")

   #원하는 데이터 추출하기
    price = soup.select_one("div.head_info > span.value").string
    #소수점 제거필요
    return int(''.join(list(filter(str.isdigit, price[:5]))))

## 쓰레드
def thread_run():
    print('=====',time.ctime(),'=====')

   
    USDKRW = get_exchange_USD()       
    
    ##print(allUpbitCoinList.keys())   
   
    threading.Timer(5, thread_run).start()    



if __name__ == "__main__":

    #빗썸
    #allBithumbCoinList = bithumb_get_ticker()
    bithumbAccess = "xxx"
    bithumbSecret = "xxx"
    bithumb = pybithumb.Bithumb(bithumbAccess, bithumbSecret)
    allBithumbCoinList = bithumb.get_current_price("ALL","KRW")
    
    #업비트
    #allUpbitCoinList = upbit_all_get_ticker()
    upbitAccess = "xxx"
    upbitSecret = "xxx"
    upbit = pyupbit.Upbit(upbitAccess, upbitSecret)
    allUpbitOriCoinList = pyupbit.get_tickers(fiat="KRW")    
    allUpbitCoinList = pyupbit.get_current_price(allUpbitOriCoinList)
    allUpbitStatus = upbit_all_get_wallet_status(upbitAccess, upbitSecret) ## 입출금상태 확인 wallet_state
    
    

    #바이낸스    
    #allBinanceCoinList = binanace_get_ticker()
    binanceAccess = "xxx"
    binanceSecret = "xxx"
    binance = Client(binanceAccess, binanceSecret)
    allBinanceCoinList = binance.get_all_tickers()
    binance_bal = binance.get_asset_balance(asset='USDT')

    #환율
    USDKRW = get_exchange_USD()
    
    ##바이낸스 업비트
    differUpbitAndBinance()

    print("*******************************빗썸시작*********************************")

    ##바이낸스 빗썸
    differBithumbAndBinance()
    #kakao.sendMsgMe("test")
    #thread_run()
   






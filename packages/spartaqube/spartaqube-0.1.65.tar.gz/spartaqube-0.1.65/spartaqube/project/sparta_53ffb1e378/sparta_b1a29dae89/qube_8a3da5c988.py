import json,base64,asyncio,subprocess,uuid,os,requests,pandas as pd
from subprocess import PIPE
from django.db.models import Q
from datetime import datetime,timedelta
import pytz
UTC=pytz.utc
from project.models_spartaqube import DBConnector,DBConnectorUserShared,PlotDBChart,PlotDBChartShared
from project.models import ShareRights
from project.sparta_53ffb1e378.sparta_95ef19463e import qube_797bc8f71d as qube_797bc8f71d
from project.sparta_53ffb1e378.sparta_faca5a317f import qube_a788482073
from project.sparta_53ffb1e378.sparta_6839de24cb import qube_59c94ebf0e as qube_59c94ebf0e
from project.sparta_53ffb1e378.sparta_faca5a317f.qube_4331948aaf import Connector as Connector
from project.logger_config import logger
def sparta_b23de933ca(json_data,user_obj):
	D='key';A=json_data;logger.debug('Call autocompelte api');logger.debug(A);B=A[D];E=A['api_func'];C=[]
	if E=='tv_symbols':C=sparta_b2946c96fd(B)
	return{'res':1,'output':C,D:B}
def sparta_b2946c96fd(key_symbol):
	F='</em>';E='<em>';B='symbol_id';G=f"https://symbol-search.tradingview.com/local_search/v3/?text={key_symbol}&hl=1&exchange=&lang=en&search_type=undefined&domain=production&sort_by_country=US";H={'http':os.environ.get('http_proxy',None),'https':os.environ.get('https_proxy',None)};C=requests.get(G,proxies=H)
	try:
		if int(C.status_code)==200:
			I=json.loads(C.text);D=I['symbols']
			for A in D:A[B]=A['symbol'].replace(E,'').replace(F,'');A['title']=A[B];A['subtitle']=A['description'].replace(E,'').replace(F,'');A['value']=A[B]
			return D
		return[]
	except:return[]
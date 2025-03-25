_C='isAuth'
_B='jsonData'
_A='res'
import json
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from project.sparta_53ffb1e378.sparta_0a2f6496d5 import qube_8fbd96b92d as qube_8fbd96b92d
from project.sparta_9e6f96b177.sparta_fed68a0eab.qube_3b035725a9 import sparta_c8ecd38ed6
from project.logger_config import logger
@csrf_exempt
def sparta_035c659038(request):A=json.loads(request.body);B=json.loads(A[_B]);return qube_8fbd96b92d.sparta_035c659038(B)
@csrf_exempt
def sparta_7753407281(request):logout(request);A={_A:1};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_476f1a545d(request):
	if request.user.is_authenticated:A=1
	else:A=0
	B={_A:1,_C:A};C=json.dumps(B);return HttpResponse(C)
def sparta_b56e3b157d(request):
	B=request;from django.contrib.auth import authenticate as F,login;from django.contrib.auth.models import User as C;G=json.loads(B.body);D=json.loads(G[_B]);H=D['email'];I=D['password'];E=0
	try:
		A=C.objects.get(email=H);A=F(B,username=A.username,password=I)
		if A is not None:login(B,A);E=1
	except C.DoesNotExist:pass
	J={_A:1,_C:E};K=json.dumps(J);return HttpResponse(K)
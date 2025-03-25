_A='jsonData'
import json,inspect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from project.sparta_53ffb1e378.sparta_1bb2aba5da import qube_34f84ec0b1 as qube_34f84ec0b1
from project.sparta_53ffb1e378.sparta_0a2f6496d5.qube_8fbd96b92d import sparta_795c1e5190
def sparta_da33569341(request):A={'res':1};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
@sparta_795c1e5190
def sparta_1790654d02(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_34f84ec0b1.sparta_1790654d02(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
def sparta_9153949604(request):
	C='userObj';B=request;D=json.loads(B.body);E=json.loads(D[_A]);F=B.user;A=qube_34f84ec0b1.sparta_9153949604(E,F)
	if A['res']==1:
		if C in list(A.keys()):login(B,A[C]);A.pop(C,None)
	G=json.dumps(A);return HttpResponse(G)
@csrf_exempt
@sparta_795c1e5190
def sparta_3f4570f203(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=A.user;E=qube_34f84ec0b1.sparta_3f4570f203(C,D);F=json.dumps(E);return HttpResponse(F)
@csrf_exempt
@sparta_795c1e5190
def sparta_e98f722e10(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_34f84ec0b1.sparta_e98f722e10(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
def sparta_2d567bf98c(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_34f84ec0b1.sparta_2d567bf98c(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
@sparta_795c1e5190
def sparta_5bc2c6f77d(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_34f84ec0b1.sparta_5bc2c6f77d(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_99bcf686ed(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_34f84ec0b1.token_reset_password_worker(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
@sparta_795c1e5190
def sparta_cc313020b1(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_34f84ec0b1.network_master_reset_password(C,A.user);E=json.dumps(D);return HttpResponse(E)
@csrf_exempt
def sparta_1b9f0731eb(request):A=json.loads(request.body);B=json.loads(A[_A]);C=qube_34f84ec0b1.sparta_1b9f0731eb(B);D=json.dumps(C);return HttpResponse(D)
@csrf_exempt
def sparta_678f81d840(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_34f84ec0b1.sparta_678f81d840(A,C);E=json.dumps(D);return HttpResponse(E)
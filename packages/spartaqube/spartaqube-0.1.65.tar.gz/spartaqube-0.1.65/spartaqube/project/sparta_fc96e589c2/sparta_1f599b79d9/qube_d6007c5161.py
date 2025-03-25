_P='Please send valid data'
_O='dist/project/auth/resetPasswordChange.html'
_N='captcha'
_M='cypress_tests@gmail.com'
_L='password'
_K='POST'
_J=False
_I='login'
_H='error'
_G='form'
_F='email'
_E='res'
_D='home'
_C='manifest'
_B='errorMsg'
_A=True
import json,hashlib,uuid
from datetime import datetime
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from django.urls import reverse
import project.sparta_9e6f96b177.sparta_fed68a0eab.qube_3b035725a9 as qube_3b035725a9
from project.forms import ConnexionForm,RegistrationTestForm,RegistrationBaseForm,RegistrationForm,ResetPasswordForm,ResetPasswordChangeForm
from project.sparta_53ffb1e378.sparta_0a2f6496d5.qube_8fbd96b92d import sparta_43c7b997ad
from project.sparta_53ffb1e378.sparta_0a2f6496d5 import qube_8fbd96b92d as qube_8fbd96b92d
from project.sparta_47a3c8f9cc.sparta_21d1831318 import qube_13dab43fe2 as qube_13dab43fe2
from project.models import LoginLocation,UserProfile
from project.logger_config import logger
def sparta_24db6f7a93():return{'bHasCompanyEE':-1}
def sparta_18caa1b5fc(request):B=request;A=qube_3b035725a9.sparta_6d69866b9f(B);A[_C]=qube_3b035725a9.sparta_092a9a9c75();A['forbiddenEmail']=conf_settings.FORBIDDEN_EMAIL;return render(B,'dist/project/auth/banned.html',A)
@sparta_43c7b997ad
def sparta_1e4a535278(request):
	C=request;B='/';A=C.GET.get(_I)
	if A is not None:D=A.split(B);A=B.join(D[1:]);A=A.replace(B,'$@$')
	return sparta_e82dcb92f5(C,A)
def sparta_293a81367c(request,redirectUrl):return sparta_e82dcb92f5(request,redirectUrl)
def sparta_e82dcb92f5(request,redirectUrl):
	E=redirectUrl;A=request;logger.debug('Welcome to loginRedirectFunc')
	if A.user.is_authenticated:return redirect(_D)
	G=_J;H='Email or password incorrect'
	if A.method==_K:
		C=ConnexionForm(A.POST)
		if C.is_valid():
			I=C.cleaned_data[_F];J=C.cleaned_data[_L];F=authenticate(username=I,password=J)
			if F:
				if qube_8fbd96b92d.sparta_fcf454e400(F):return sparta_18caa1b5fc(A)
				login(A,F);K,L=qube_3b035725a9.sparta_2b3bf02cee();LoginLocation.objects.create(user=F,hostname=K,ip=L,date_login=datetime.now())
				if E is not None:
					D=E.split('$@$');D=[A for A in D if len(A)>0]
					if len(D)>1:M=D[0];return redirect(reverse(M,args=D[1:]))
					return redirect(E)
				return redirect(_D)
			else:G=_A
		else:G=_A
	C=ConnexionForm();B=qube_3b035725a9.sparta_6d69866b9f(A);B.update(qube_3b035725a9.sparta_bc3763369d(A));B[_C]=qube_3b035725a9.sparta_092a9a9c75();B[_G]=C;B[_H]=G;B['redirectUrl']=E;B[_B]=H;B.update(sparta_24db6f7a93());return render(A,'dist/project/auth/login.html',B)
def sparta_c6ba6fbdd3(request):
	B='public@spartaqube.com';A=User.objects.filter(email=B).all()
	if A.count()>0:C=A[0];login(request,C)
	return redirect(_D)
@sparta_43c7b997ad
def sparta_06ead5c77a(request):
	A=request
	if A.user.is_authenticated:return redirect(_D)
	E='';D=_J;F=qube_8fbd96b92d.sparta_f845278f09()
	if A.method==_K:
		if F:B=RegistrationForm(A.POST)
		else:B=RegistrationBaseForm(A.POST)
		if B.is_valid():
			I=B.cleaned_data;H=None
			if F:
				H=B.cleaned_data['code']
				if not qube_8fbd96b92d.sparta_6a0ca5372e(H):D=_A;E='Wrong guest code'
			if not D:
				J=A.META['HTTP_HOST'];G=qube_8fbd96b92d.sparta_035c659038(I,J)
				if int(G[_E])==1:K=G['userObj'];login(A,K);return redirect(_D)
				else:D=_A;E=G[_B]
		else:D=_A;E=B.errors.as_data()
	if F:B=RegistrationForm()
	else:B=RegistrationBaseForm()
	C=qube_3b035725a9.sparta_6d69866b9f(A);C.update(qube_3b035725a9.sparta_bc3763369d(A));C[_C]=qube_3b035725a9.sparta_092a9a9c75();C[_G]=B;C[_H]=D;C[_B]=E;C.update(sparta_24db6f7a93());return render(A,'dist/project/auth/registration.html',C)
def sparta_aec52050ba(request):A=request;B=qube_3b035725a9.sparta_6d69866b9f(A);B[_C]=qube_3b035725a9.sparta_092a9a9c75();return render(A,'dist/project/auth/registrationPending.html',B)
def sparta_c151fccd74(request,token):
	A=request;B=qube_8fbd96b92d.sparta_84d6e743f4(token)
	if int(B[_E])==1:C=B['user'];login(A,C);return redirect(_D)
	D=qube_3b035725a9.sparta_6d69866b9f(A);D[_C]=qube_3b035725a9.sparta_092a9a9c75();return redirect(_I)
def sparta_8cc92ef1e6(request):logout(request);return redirect(_I)
def sparta_e03498c682():
	from project.models import PlotDBChartShared as B,PlotDBChart,DashboardShared as C,NotebookShared as D,KernelShared as E,DBConnectorUserShared as F;A=_M;print('Destroy cypress user');G=B.objects.filter(user__email=A).all()
	for H in G:H.delete()
	I=C.objects.filter(user__email=A).all()
	for J in I:J.delete()
	K=D.objects.filter(user__email=A).all()
	for L in K:L.delete()
	M=E.objects.filter(user__email=A).all()
	for N in M:N.delete()
	O=F.objects.filter(user__email=A).all()
	for P in O:P.delete()
def sparta_3794e37925(request):
	A=request;B=_M;from project.sparta_53ffb1e378.sparta_784a241164.qube_8c9561c7c1 import sparta_c16fd00145 as C;C(A.user);sparta_e03498c682()
	if A.user.is_authenticated:
		if A.user.email==B:A.user.delete()
	logout(A);return redirect(_I)
def sparta_d5ed163791(request):A={_E:-100,_B:'You are not logged...'};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_3d8ee85896(request):
	A=request;E='';F=_J
	if A.method==_K:
		B=ResetPasswordForm(A.POST)
		if B.is_valid():
			H=B.cleaned_data[_F];I=B.cleaned_data[_N];G=qube_8fbd96b92d.sparta_3d8ee85896(H.lower(),I)
			try:
				if int(G[_E])==1:C=qube_3b035725a9.sparta_6d69866b9f(A);C.update(qube_3b035725a9.sparta_bc3763369d(A));B=ResetPasswordChangeForm(A.POST);C[_C]=qube_3b035725a9.sparta_092a9a9c75();C[_G]=B;C[_F]=H;C[_H]=F;C[_B]=E;return render(A,_O,C)
				elif int(G[_E])==-1:E=G[_B];F=_A
			except Exception as J:logger.debug('exception ');logger.debug(J);E='Could not send reset email, please try again';F=_A
		else:E=_P;F=_A
	else:B=ResetPasswordForm()
	D=qube_3b035725a9.sparta_6d69866b9f(A);D.update(qube_3b035725a9.sparta_bc3763369d(A));D[_C]=qube_3b035725a9.sparta_092a9a9c75();D[_G]=B;D[_H]=F;D[_B]=E;D.update(sparta_24db6f7a93());return render(A,'dist/project/auth/resetPassword.html',D)
@csrf_exempt
def sparta_29eb898050(request):
	D=request;E='';B=_J
	if D.method==_K:
		C=ResetPasswordChangeForm(D.POST)
		if C.is_valid():
			I=C.cleaned_data['token'];F=C.cleaned_data[_L];J=C.cleaned_data['password_confirmation'];K=C.cleaned_data[_N];G=C.cleaned_data[_F].lower()
			if len(F)<6:E='Your password must be at least 6 characters';B=_A
			if F!=J:E='The two passwords must be identical...';B=_A
			if not B:
				H=qube_8fbd96b92d.sparta_29eb898050(K,I,G.lower(),F)
				try:
					if int(H[_E])==1:L=User.objects.get(username=G);login(D,L);return redirect(_D)
					else:E=H[_B];B=_A
				except Exception as M:E='Could not change your password, please try again';B=_A
		else:E=_P;B=_A
	else:return redirect('reset-password')
	A=qube_3b035725a9.sparta_6d69866b9f(D);A.update(qube_3b035725a9.sparta_bc3763369d(D));A[_C]=qube_3b035725a9.sparta_092a9a9c75();A[_G]=C;A[_H]=B;A[_B]=E;A[_F]=G;A.update(sparta_24db6f7a93());return render(D,_O,A)
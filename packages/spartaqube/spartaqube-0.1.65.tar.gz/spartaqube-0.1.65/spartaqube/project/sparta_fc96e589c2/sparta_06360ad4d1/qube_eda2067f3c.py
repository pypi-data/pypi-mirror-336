from urllib.parse import urlparse,urlunparse
from django.contrib.auth.decorators import login_required
from django.conf import settings as conf_settings
from django.shortcuts import render
import project.sparta_9e6f96b177.sparta_fed68a0eab.qube_3b035725a9 as qube_3b035725a9
from project.models import UserProfile
from project.sparta_53ffb1e378.sparta_0a2f6496d5.qube_8fbd96b92d import sparta_43c7b997ad
from project.sparta_fc96e589c2.sparta_1f599b79d9.qube_d6007c5161 import sparta_24db6f7a93
@sparta_43c7b997ad
@login_required(redirect_field_name='login')
def sparta_ccd2679deb(request,idSection=1):
	B=request;D=UserProfile.objects.get(user=B.user);E=D.avatar
	if E is not None:E=D.avatar.avatar
	C=urlparse(conf_settings.URL_TERMS)
	if not C.scheme:C=urlunparse(C._replace(scheme='http'))
	F={'item':1,'idSection':idSection,'userProfil':D,'avatar':E,'url_terms':C};A=qube_3b035725a9.sparta_6d69866b9f(B);A.update(qube_3b035725a9.sparta_c34211e67a(B.user));A.update(F);G='';A['accessKey']=G;A['menuBar']=4;A.update(sparta_24db6f7a93());return render(B,'dist/project/auth/settings.html',A)
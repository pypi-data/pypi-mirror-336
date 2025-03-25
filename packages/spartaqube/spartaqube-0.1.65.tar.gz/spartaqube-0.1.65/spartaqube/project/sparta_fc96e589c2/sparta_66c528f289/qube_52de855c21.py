import os,json,getpass,platform
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
import project.sparta_9e6f96b177.sparta_fed68a0eab.qube_3b035725a9 as qube_3b035725a9
from project.sparta_53ffb1e378.sparta_0a2f6496d5.qube_8fbd96b92d import sparta_43c7b997ad
from project.sparta_53ffb1e378.sparta_6839de24cb import qube_48847ac5ce as qube_48847ac5ce
from project.sparta_53ffb1e378.sparta_2c2de249fd import qube_d35c863df6 as qube_d35c863df6
def sparta_37edf152d8():
	A=platform.system()
	if A=='Windows':return'windows'
	elif A=='Linux':return'linux'
	elif A=='Darwin':return'mac'
	else:return
@csrf_exempt
@sparta_43c7b997ad
@login_required(redirect_field_name='login')
def sparta_99e9413e0f(request):
	E='template';D='developer';B=request
	if not conf_settings.IS_DEV_VIEW_ENABLED:A=qube_3b035725a9.sparta_6d69866b9f(B);return render(B,'dist/project/homepage/homepage.html',A)
	A=qube_3b035725a9.sparta_6d69866b9f(B);A['menuBar']=12;F=qube_3b035725a9.sparta_c34211e67a(B.user);A.update(F);A['bCodeMirror']=True;G=os.path.dirname(__file__);C=os.path.dirname(os.path.dirname(G));H=os.path.join(C,'static');I=os.path.join(H,'js',D,E,'frontend');A['frontend_path']=I;J=os.path.dirname(C);K=os.path.join(J,'django_app_template',D,E,'backend');A['backend_path']=K;return render(B,'dist/project/developer/developerExamples.html',A)
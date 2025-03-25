_C='bCodeMirror'
_B='menuBar'
_A=True
import os,json,getpass,platform
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import project.sparta_9e6f96b177.sparta_fed68a0eab.qube_3b035725a9 as qube_3b035725a9
from project.sparta_53ffb1e378.sparta_0a2f6496d5.qube_8fbd96b92d import sparta_43c7b997ad
from project.sparta_53ffb1e378.sparta_6839de24cb import qube_48847ac5ce as qube_48847ac5ce
from project.sparta_53ffb1e378.sparta_2c2de249fd import qube_d35c863df6 as qube_d35c863df6
from project.sparta_53ffb1e378.sparta_fb4fb1662f.qube_bb1f3cf253 import sparta_21537dcf3c
@csrf_exempt
@sparta_43c7b997ad
@login_required(redirect_field_name='login')
def sparta_48a8aae789(request):
	B=request;C=B.GET.get('edit')
	if C is None:C='-1'
	A=qube_3b035725a9.sparta_6d69866b9f(B);A[_B]=9;E=qube_3b035725a9.sparta_c34211e67a(B.user);A.update(E);A[_C]=_A;A['edit_chart_id']=C
	def F(path):
		A=Path(path)
		if not A.exists():A.mkdir(parents=_A)
	G=sparta_21537dcf3c();D=os.path.join(G,'dashboard');F(D);A['default_project_path']=D;return render(B,'dist/project/dashboard/dashboard.html',A)
@csrf_exempt
def sparta_a16c15f8bb(request,id):
	A=request
	if id is None:B=A.GET.get('id')
	else:B=id
	return sparta_1a99bdee4e(A,B)
def sparta_1a99bdee4e(request,dashboard_id,session='-1'):
	G='res';E=dashboard_id;B=request;C=False
	if E is None:C=_A
	else:
		D=qube_d35c863df6.has_dashboard_access(E,B.user);H=D[G]
		if H==-1:C=_A
	if C:return sparta_48a8aae789(B)
	A=qube_3b035725a9.sparta_6d69866b9f(B);A[_B]=9;I=qube_3b035725a9.sparta_c34211e67a(B.user);A.update(I);A[_C]=_A;F=D['dashboard_obj'];A['b_require_password']=0 if D[G]==1 else 1;A['dashboard_id']=F.dashboard_id;A['dashboard_name']=F.name;A['bPublicUser']=B.user.is_anonymous;A['session']=str(session);return render(B,'dist/project/dashboard/dashboardRun.html',A)
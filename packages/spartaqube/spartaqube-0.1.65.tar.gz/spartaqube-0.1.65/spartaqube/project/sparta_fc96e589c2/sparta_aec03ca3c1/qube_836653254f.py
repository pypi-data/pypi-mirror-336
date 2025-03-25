from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from project.sparta_53ffb1e378.sparta_0a2f6496d5.qube_8fbd96b92d import sparta_43c7b997ad
from project.sparta_53ffb1e378.sparta_6bbcfb14d9 import qube_9b2cc9d4ce as qube_9b2cc9d4ce
from project.models import UserProfile
import project.sparta_9e6f96b177.sparta_fed68a0eab.qube_3b035725a9 as qube_3b035725a9
@sparta_43c7b997ad
@login_required(redirect_field_name='login')
def sparta_e66a59087d(request):
	E='avatarImg';B=request;A=qube_3b035725a9.sparta_6d69866b9f(B);A['menuBar']=-1;F=qube_3b035725a9.sparta_c34211e67a(B.user);A.update(F);A[E]='';C=UserProfile.objects.filter(user=B.user)
	if C.count()>0:
		D=C[0];G=D.avatar
		if G is not None:H=D.avatar.image64;A[E]=H
	A['bInvertIcon']=0;return render(B,'dist/project/helpCenter/helpCenter.html',A)
@sparta_43c7b997ad
@login_required(redirect_field_name='login')
def sparta_da5c1c48b7(request):
	A=request;B=UserProfile.objects.filter(user=A.user)
	if B.count()>0:C=B[0];C.has_open_tickets=False;C.save()
	return sparta_e66a59087d(A)
_A='jsonData'
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from project.models import UserProfile
from project.sparta_53ffb1e378.sparta_8c0459ef04 import qube_d2013bc755 as qube_d2013bc755
from project.sparta_53ffb1e378.sparta_6bbcfb14d9 import qube_9b2cc9d4ce as qube_9b2cc9d4ce
from project.sparta_53ffb1e378.sparta_0a2f6496d5.qube_8fbd96b92d import sparta_795c1e5190
@csrf_exempt
@sparta_795c1e5190
def sparta_cc5b389588(request):
	B=request;I=json.loads(B.body);C=json.loads(I[_A]);A=B.user;D=0;E=UserProfile.objects.filter(user=A)
	if E.count()>0:
		F=E[0]
		if F.has_open_tickets:
			C['userId']=F.user_profile_id;G=qube_9b2cc9d4ce.sparta_03a7eb0564(A)
			if G['res']==1:D=int(G['nbNotifications'])
	H=qube_d2013bc755.sparta_cc5b389588(C,A);H['nbNotificationsHelpCenter']=D;J=json.dumps(H);return HttpResponse(J)
@csrf_exempt
@sparta_795c1e5190
def sparta_ecc5b92461(request):A=request;B=json.loads(A.body);C=json.loads(B[_A]);D=qube_d2013bc755.sparta_457598f116(C,A.user);E=json.dumps(D);return HttpResponse(E)
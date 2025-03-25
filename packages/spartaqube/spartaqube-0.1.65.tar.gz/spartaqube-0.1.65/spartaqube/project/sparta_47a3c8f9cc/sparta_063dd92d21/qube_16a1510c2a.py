import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from project.sparta_53ffb1e378.sparta_0a2f6496d5.qube_8fbd96b92d import sparta_795c1e5190
from project.sparta_53ffb1e378.sparta_459734b040 import qube_37b77d43a2 as qube_37b77d43a2
@csrf_exempt
@sparta_795c1e5190
def sparta_0347000c2f(request):A=request;B=json.loads(A.body);C=json.loads(B['jsonData']);D=A.user;E=qube_37b77d43a2.sparta_0347000c2f(C,D);F=json.dumps(E);return HttpResponse(F)
_A='utf-8'
import os,json,base64,hashlib,random
from cryptography.fernet import Fernet
def sparta_e6f1a97418():A='__API_AUTH__';A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_01ec00f059(objectToCrypt):A=objectToCrypt;C=sparta_e6f1a97418();D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_a89e1d4c28(apiAuth):A=apiAuth;B=sparta_e6f1a97418();C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_652a263eaf(kCrypt):A='__SQ_AUTH__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_ef43e2f471(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_652a263eaf(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_3c09f9e6b2(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_652a263eaf(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_da0f1da911(kCrypt):A='__SQ_EMAIL__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_a31fcdc918(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_da0f1da911(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_a9e698f42f(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_da0f1da911(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_4085983b84(kCrypt):A='__SQ_KEY_SSO_CRYPT__'+str(kCrypt);A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_e87e56bc64(objectToCrypt,kCrypt):A=objectToCrypt;C=sparta_4085983b84(kCrypt);D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_77f1612122(objectToDecrypt,kCrypt):A=objectToDecrypt;B=sparta_4085983b84(kCrypt);C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
def sparta_2ed16ef11d():A='__SQ_IPYNB_SQ_METADATA__';A=A.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A
def sparta_c37c8fc878(objectToCrypt):A=objectToCrypt;C=sparta_2ed16ef11d();D=Fernet(C);A=A.encode(_A);B=D.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_9d8f675dfb(objectToDecrypt):A=objectToDecrypt;B=sparta_2ed16ef11d();C=Fernet(B);A=base64.b64decode(A);return C.decrypt(A).decode(_A)
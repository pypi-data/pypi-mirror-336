_B=False
_A=None
from pydantic import BaseModel
class CompareGroup(BaseModel):name:str;data:dict|_A
class CompareErrFloats(BaseModel):is_relative:bool;value:float;test:float;reference:float
class CompareErr(BaseModel):err:CompareErrFloats|_A;msg:int;group:int|_A=_A;info:dict|_A=_A
SEVERITY_ERROR='error'
SEVERITY_WARNING='warning'
class CompareErrors:
	def __init__(A,nb_max,ignore_warnings=_B):A.nb_max=nb_max;A.ignore_warnings=ignore_warnings;A.errors={SEVERITY_ERROR:[],SEVERITY_WARNING:[]};A.count=0;A.limit_reached=_B;A.messages=[];A.messages_map={};A.groups=[]
	def add_group(A,name,data=_A):B=len(A.groups);A.groups.append(CompareGroup(name=name,data=data));return B
	def add(A,severity,message,comp_err,group_idx=_A,info=_A):
		D=severity;C=message
		if A.ignore_warnings and D==SEVERITY_WARNING:return _B
		A.count+=1;B=A.messages_map.get(C)
		if B is _A:B=len(A.messages);A.messages.append(C);A.messages_map[C]=B
		A.errors[D].append(CompareErr(err=comp_err,msg=B,group=group_idx,info=info))
		if A.count>=A.nb_max:A.limit_reached=True;return True
	def get_data(B):
		A={'messages':B.messages,'groups':[A.model_dump()for A in B.groups]}
		for(C,D)in B.errors.items():A[C]=[A.model_dump()for A in D];A[C+'_nb']=len(A[C])
		return A
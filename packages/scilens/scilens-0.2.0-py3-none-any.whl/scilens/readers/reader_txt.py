_F='floats'
_E='lines'
_D=True
_C=False
_B='line'
_A=None
from scilens.readers.reader_interface import ReaderInterface
from scilens.readers.transform import string_2_floats
from scilens.config.models import ReaderTxtConfig
from scilens.components.compare_errors import SEVERITY_ERROR
from scilens.components.compare_floats import CompareFloats
class ReaderTxt(ReaderInterface):
	category='datalines';extensions=['TXT']
	def read(A,config):
		F='_';B=config;A.reader_options=B;A.get_lines_pre=1;A.get_lines_post=1
		if B.report_lines:
			C=_C
			for(I,G)in B.report_lines.items():
				if I==A.origin.short_name:C=_D;A.get_lines_pre=G.pre;A.get_lines_post=G.post
			if not C and B.report_lines.get(F):A.get_lines_pre=B.report_lines[F].pre;A.get_lines_post=B.report_lines[F].post
		D=_A
		if B.ignore:
			C=_C
			for(I,G)in B.ignore.items():
				if I==A.origin.short_name:C=_D;D=G
			if not C and B.ignore.get(F):D=B.ignore[F]
		K=open(A.origin.path,'r',encoding=A.encoding);A.raw_lines=K.readlines();K.close();A.raw_lines_number=len(A.raw_lines);E=[]
		if D:
			C,O=A.find_patterns_lines_nb([A.pattern for A in D])
			for(P,L)in enumerate(D):
				H=O[P][_E]
				if H:H=A.get_raw_siblings_nb(H,pre=L.pre,post=L.post);E+=H
			E=list(set(E));E.sort()
		A.ignore_patterns=[A.pattern for A in D]if D else[];A.ignore_lines=E;A.ignore_lines_number=len(E);A.curves=A.curve_parser(A.raw_lines)if A.curve_parser else _A;J=[]
		for(Q,R)in enumerate(A.raw_lines):
			M=string_2_floats(R)
			if M:
				N=Q+1
				if not N in E:J.append({_B:N,_F:M})
		A.floats_lines=J;A.floats_lines_number=len(J)
		if B.error_rule_patterns:
			C,S=A.find_patterns_lines_nb(B.error_rule_patterns);A.read_data['error_rule_patterns']={'found':C,'data':S}
			if C:A.read_error='String error pattern found'
	def compare(I,compare_floats,param_reader,param_is_ref=_D):
		K=param_is_ref;J=param_reader;D=compare_floats;A=I if K else J;B=I if not K else J;E=0;C=_C;Y=[]
		if A.floats_lines_number!=B.floats_lines_number:T=f"Nb number lines 1: {A.floats_lines_number} 2: {B.floats_lines_number} different";return T,_A
		L=A.floats_lines;U=B.floats_lines
		for M in range(len(L)):
			F=L[M];G=U[M];H=F[_F];N=G[_F];O={'line_nb_1':F[_B],'line_nb_2':G[_B],'line_1':A.get_raw_lines(F[_B]),'line_2':B.get_raw_lines(G[_B])}
			if len(H)!=len(N):
				if not C:E+=1;C=D.compare_errors.add(SEVERITY_ERROR,'Not same numbers number in the lines',_A,info=O)
				continue
			for P in range(len(H)):
				Q=H[P];R=N[P];V=Q-R
				if V==0:continue
				else:
					E+=1
					if not C:
						W,X,S=D.compare_2_values(Q,R)
						if S:C=D.compare_errors.add(W,X,S,info=O)
		return _A,{'type':_E,'total_diffs':E}
	def find_patterns_lines_nb(D,patterns):
		A=patterns;B=_C;map={A:[]for A in A}
		for(E,F)in enumerate(D.raw_lines):
			for C in A:
				if F.find(C)!=-1:map[C].append(E+1);B=_D
		return B,[{'pattern':A,_E:map[A]}for A in A]
	def get_raw_siblings_nb(A,lines_nb_array,pre=_A,post=_A):
		B=[]
		for C in lines_nb_array:
			min=C-(pre if pre is not _A else A.get_lines_pre);max=C+(post if post is not _A else A.get_lines_post)+1
			if min<0:min=0
			if max>A.raw_lines_number+1:max=A.raw_lines_number+1
			for D in range(min,max):
				if D not in B:B.append(D)
		return B
	def get_raw_lines(A,line_nb,pre=_A,post=_A):
		B=line_nb;min=B-1-(pre if pre is not _A else A.get_lines_pre);max=B-1+(post if post is not _A else A.get_lines_post)+1
		if min<0:min=0
		if max>A.raw_lines_number:max=A.raw_lines_number
		return''.join([A.raw_lines[B]for B in range(min,max)])
	def class_info(A):return{'raw_lines_number':A.raw_lines_number,'ignore_patterns':A.ignore_patterns,'ignore_lines_number':A.ignore_lines_number,'ignore_lines':A.ignore_lines,'floats_lines_number':A.floats_lines_number,'curves':A.curves}
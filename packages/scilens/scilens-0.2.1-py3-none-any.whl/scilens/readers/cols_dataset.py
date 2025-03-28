_E='charts'
_D='x_index'
_C='csv_col_index'
_B='curves'
_A=None
from dataclasses import dataclass,field
from scilens.components.compare_floats import CompareFloats
from scilens.config.models.reader_format_cols_curve import ReaderCurveParserNameConfig
@dataclass
class ColsDataset:cols_count:int=0;rows_count:int=0;names:list[str]=field(default_factory=lambda:[]);numeric_col_indexes:list[int]=field(default_factory=lambda:[]);data:list[list[float]]=field(default_factory=lambda:[]);origin_line_nb:list[int]=field(default_factory=lambda:[])
@dataclass
class ColsCurves:type:str;info:dict;curves:dict
def cols_dataset_get_curves_col_x(cols_dataset,col_x):
	I='title';B=col_x;A=cols_dataset;E={}
	if isinstance(B,int):
		C=B-1
		if C<0 or C>=A.cols_count:raise Exception('curve parser col_x: col_index is out of range.')
	if isinstance(B,str):B=[B]
	if isinstance(B,list):
		G=[A for(A,C)in enumerate(A.names)if C in B]
		if len(G)==0:return _A,E
		C=G[0]
	E[_D]=C;J=[B for(A,B)in enumerate(A.numeric_col_indexes)if A!=C];F=[];H=[]
	for D in J:B=A.data[C];K=A.data[D];L={I:A.names[D],'short_title':A.names[D],'series':[[B[A],K[A]]for A in range(A.rows_count)],_C:D};F+=[L];M={I:A.names[D],'type':'simple','xaxis':A.names[C],'yaxis':A.names[D],_B:[len(F)-1]};H+=[M]
	return{_B:F,_E:H},E
def compare(compare_floats,reader_test,reader_ref,cols_curve):
	Q='error';J=compare_floats;I='Errors limit reached';E=reader_ref;C=cols_curve;A=reader_test
	if len(A.numeric_col_indexes)!=len(E.numeric_col_indexes):R=f"Number Float columns indexes are different: {len(A.numeric_col_indexes)} != {len(E.numeric_col_indexes)}";return R,_A
	K=0;D=[''for A in range(A.cols_count)];L=_A;F=_A
	if C and C.type==ReaderCurveParserNameConfig.COL_X:M=C.info[_D];L=A.data[M];F=A.names[M]
	G=False
	for B in range(A.cols_count):
		if B not in A.numeric_col_indexes:continue
		if G:D[B]=I;continue
		S=A.data[B];T=E.data[B];U=J.compare_errors.add_group(A.names[B],data={'info_prefix':F}if F else _A);V,W,N=J.compare_vectors(S,T,group_idx=U,info_vector=L);K+=W
		if V:G=True;D[B]=I;continue
		if N[Q]>0:D[B]=f"{N[Q]} comparison errors"
	if C:
		for O in C.curves[_E]:
			P=0
			for X in O[_B]:
				H=C.curves[_B][X]
				if D[H[_C]]:H['comparison_error']=D[H[_C]];P+=1
			O['comparison']={'curves_nb_with_error':P}
	Y=I if G else _A;return Y,{'type':'vectors','total_diffs':K,'cols_has_error':D}
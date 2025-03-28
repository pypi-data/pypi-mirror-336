_E='charts'
_D='x_index'
_C='csv_col_index'
_B='curves'
_A=None
import logging,csv
from scilens.readers.reader_interface import ReaderInterface
from scilens.config.models import ReaderCsvConfig
from scilens.config.models.reader_format_cols_curve import ReaderCurveParserNameConfig
from scilens.components.compare_floats import CompareFloats
def is_num(x):
	try:return float(x)
	except ValueError:return
def csv_row_detect_header(first_row):
	A=first_row
	if all(not A.isdigit()for A in A):return True,A
	else:return False,[f"Column {A}"for(A,B)in enumerate(A)]
def csv_row_detect_cols_num(row):return[A for(A,B)in enumerate(row)if is_num(B)!=_A]
def csv_detect(path,delimiter,quotechar):
	with open(path,'r')as B:A=csv.reader(B,delimiter=delimiter,quotechar=quotechar);C=next(A);D,E=csv_row_detect_header(C);F=next(A);G=csv_row_detect_cols_num(F);return D,E,G
class ReaderCsv(ReaderInterface):
	category='datalines';extensions=['CSV']
	def read(A,reader_options):
		B=reader_options;A.reader_options=B;C,G,H=csv_detect(A.origin.path,A.reader_options.delimiter,A.reader_options.quotechar);A.has_header=C;A.cols=G;A.numeric_col_indexes=H
		if B.ignore_columns:
			if not C:raise Exception('Ignore columns is not supported without header.')
			A.numeric_col_indexes=[C for C in A.numeric_col_indexes if A.cols[C]not in B.ignore_columns]
		E=open(A.origin.path,'r',encoding=A.encoding);I=csv.reader(E,delimiter=A.reader_options.delimiter,quotechar=A.reader_options.quotechar);D=[]
		for J in I:D+=[J]
		if C:D.pop(0)
		E.close();A.data_rows=D;A.raw_lines_number=len(A.data_rows)+(1 if C else 0);A.curves=_A
		if B.curve_parser:
			if B.curve_parser.name==ReaderCurveParserNameConfig.COL_X:
				A.curves,K=A._get_curves_col_x(B.curve_parser.parameters.x)
				if A.curves:A.curves_parser_type=B.curve_parser.name;A.curves_info=K
			elif B.curve_parser.name==ReaderCurveParserNameConfig.COLS_COUPLE:raise NotImplementedError('cols_couple not implemented')
			else:raise Exception('Curve parser not supported.')
		A.cols_data=[_A]*len(A.cols)
		for F in A.numeric_col_indexes:A.cols_data[F]=[float(A[F])for A in D]
	def compare(A,compare_floats,param_reader,param_is_ref=True):
		U='error';M=param_is_ref;L=param_reader;K=compare_floats;J='Errors limit reached';C=A if M else L;E=A if not M else L
		if len(C.numeric_col_indexes)!=len(E.numeric_col_indexes):V=f"Number Float columns indexes are different: {len(C.numeric_col_indexes)} != {len(E.numeric_col_indexes)}";return V,_A
		N=0;D=[''for A in C.cols];O=_A;F=_A
		if A.curves and A.curves_parser_type==ReaderCurveParserNameConfig.COL_X:P=A.curves_info[_D];O=C.cols_data[P];F=A.cols[P]
		G=False
		for B in range(len(C.cols_data)):
			if C.cols_data[B]==_A:continue
			logging.debug(f"Comparing {A.cols[B]}")
			if G:D[B]=J;continue
			W=C.cols_data[B];X=E.cols_data[B];Y=K.compare_errors.add_group(A.cols[B],data={'info_prefix':F}if F else _A);Q,R,H=K.compare_vectors(W,X,group_idx=Y,info_vector=O);N+=R;logging.debug(f"limit_reached, diffs_count, counts: {Q}, {R}, {H}")
			if Q:G=True;D[B]=J;continue
			if H[U]>0:D[B]=f"{H[U]} comparison errors"
		if A.curves:
			for S in A.curves[_E]:
				T=0
				for Z in S[_B]:
					I=A.curves[_B][Z]
					if D[I[_C]]:I['comparison_error']=D[I[_C]];T+=1
				S['comparison']={'curves_nb_with_error':T}
		a=J if G else _A;return a,{'type':'vectors','total_diffs':N,'cols_has_error':D}
	def class_info(A):return{'cols':A.cols,'raw_lines_number':A.raw_lines_number,_B:A.curves}
	def _get_curves_col_x(E,col_x):
		J='title';A=col_x;F={};B=E.cols
		if isinstance(A,int):
			C=A-1
			if C<0 or C>=len(B):raise Exception('curve parser col_x: col_index is out of range.')
		if isinstance(A,str):A=[A]
		if isinstance(A,list):
			H=[B for(B,C)in enumerate(B)if C in A]
			if len(H)==0:return _A,F
			C=H[0]
		F[_D]=C;K=[B for(A,B)in enumerate(E.numeric_col_indexes)if A!=C];G=[];I=[]
		for D in K:L={J:B[D],'short_title':B[D],'series':[[float(A[C]),float(A[D])]for A in E.data_rows],_C:D};G+=[L];M={J:B[D],'type':'simple','xaxis':B[C],'yaxis':B[D],_B:[len(G)-1]};I+=[M]
		return{_B:G,_E:I},F
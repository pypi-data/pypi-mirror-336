import logging,csv
from scilens.readers.reader_interface import ReaderInterface
from scilens.readers.cols_dataset import ColsDataset,ColsCurves,cols_dataset_get_curves_col_x,compare
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
def csv_row_detect_cols_num(row):return[A for(A,B)in enumerate(row)if is_num(B)!=None]
def csv_detect(path,delimiter,quotechar):
	with open(path,'r')as B:A=csv.reader(B,delimiter=delimiter,quotechar=quotechar);C=next(A);D,E=csv_row_detect_header(C);F=next(A);G=csv_row_detect_cols_num(F);return D,E,G
class ReaderCsv(ReaderInterface):
	category='datalines';extensions=['CSV']
	def read(A,reader_options):
		C=reader_options;A.reader_options=C;D,E,K=csv_detect(A.origin.path,A.reader_options.delimiter,A.reader_options.quotechar);A.has_header=D;A.cols=E;A.numeric_col_indexes=K
		if C.ignore_columns:
			if not D:raise Exception('Ignore columns is not supported without header.')
			A.numeric_col_indexes=[B for B in A.numeric_col_indexes if A.cols[B]not in C.ignore_columns]
		H=len(E);B=ColsDataset(cols_count=H,names=E,numeric_col_indexes=A.numeric_col_indexes,data=[[]for A in range(H)]);I=open(A.origin.path,'r',encoding=A.encoding);L=csv.reader(I,delimiter=A.reader_options.delimiter,quotechar=A.reader_options.quotechar);F=0
		for M in L:
			F+=1
			if D and F==1:continue
			for(J,G)in enumerate(M):
				if J in B.numeric_col_indexes:G=float(G)
				B.data[J].append(G)
			B.origin_line_nb.append(F)
		B.rows_count=len(B.origin_line_nb);I.close();A.cols_dataset=B;A.raw_lines_number=B.rows_count+(1 if D else 0);A.curves=None
		if C.curve_parser:
			if C.curve_parser.name==ReaderCurveParserNameConfig.COL_X:
				A.curves,N=cols_dataset_get_curves_col_x(B,C.curve_parser.parameters.x)
				if A.curves:A.cols_curve=ColsCurves(type=ReaderCurveParserNameConfig.COL_X,info=N,curves=A.curves)
			elif C.curve_parser.name==ReaderCurveParserNameConfig.COLS_COUPLE:raise NotImplementedError('cols_couple not implemented')
			else:raise Exception('Curve parser not supported.')
	def compare(A,compare_floats,param_reader,param_is_ref=True):C=param_is_ref;B=param_reader;D=A.cols_dataset if C else B.cols_dataset;E=A.cols_dataset if not C else B.cols_dataset;F=A.cols_curve;return compare(compare_floats,D,E,F)
	def class_info(A):return{'cols':A.cols,'raw_lines_number':A.raw_lines_number,'curves':A.curves}
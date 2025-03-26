import logging,re
from scilens.readers.transform import string_2_float
from scilens.readers.reader_interface import ReaderInterface
from scilens.readers.cols_dataset import ColsDataset,ColsCurves,cols_dataset_get_curves_col_x,compare
from scilens.config.models import ReaderTxtFixedColsConfig
from scilens.config.models.reader_format_cols_curve import ReaderCurveParserNameConfig
from scilens.components.compare_floats import CompareFloats
class ReaderTxtFixedCols(ReaderInterface):
	category='datalines';extensions=['DAT']
	def read(B,reader_options):
		A=reader_options;B.reader_options=A;J=open(B.origin.path,'r',encoding=B.encoding);K=A.column_widths;L=A.ignore_lines_patterns;D=len(K);C=ColsDataset(cols_count=D,names=[f"Column {A+1}"for A in range(D)],numeric_col_indexes=[A for A in range(D)],data=[[]for A in range(D)]);E=None;G=0
		for F in J:
			G+=1
			if L:
				M=False
				for P in L:
					if bool(re.match(P,F)):M=True;break
				if M:continue
			if A.has_header:
				if not E:
					E=F.strip();H=E
					if A.has_header_ignore:
						for Q in A.has_header_ignore:H=H.replace(Q,'')
					C.names=H.split();continue
				elif A.has_header_repetition and E==F.strip():continue
			I=0;N=0
			for O in K:R=F[I:I+O].strip();S=string_2_float(R);C.data[N].append(S);I+=O;N+=1
			C.origin_line_nb.append(G)
		C.rows_count=len(C.origin_line_nb);J.close();B.cols_dataset=C;B.raw_lines_number=G;print(C);B.curves=None
		if A.curve_parser:
			if A.curve_parser.name==ReaderCurveParserNameConfig.COL_X:
				B.curves,T=cols_dataset_get_curves_col_x(C,A.curve_parser.parameters.x)
				if B.curves:B.cols_curve=ColsCurves(type=ReaderCurveParserNameConfig.COL_X,info=T,curves=B.curves)
			elif A.curve_parser.name==ReaderCurveParserNameConfig.COLS_COUPLE:raise NotImplementedError('cols_couple not implemented')
			else:raise Exception('Curve parser not supported.')
	def compare(A,compare_floats,param_reader,param_is_ref=True):C=param_is_ref;B=param_reader;D=A.cols_dataset if C else B.cols_dataset;E=A.cols_dataset if not C else B.cols_dataset;F=A.cols_curve;return compare(compare_floats,D,E,F)
	def class_info(A):return{'cols':A.cols_dataset.names,'raw_lines_number':A.raw_lines_number,'curves':A.curves}
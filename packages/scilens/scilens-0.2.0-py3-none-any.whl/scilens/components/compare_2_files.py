import os
from scilens.run.task_context import TaskContext
from scilens.components.file_reader import FileReader
from scilens.components.compare_errors import CompareErrors,SEVERITY_ERROR
from scilens.components.compare_floats import CompareFloats
class Compare2Files:
	def __init__(A,context):A.context=context
	def compare(B,path_test,path_ref):
		Q='comparison_errors';P='comparison';M='reader';J='error';I='ref';H='test';E='path';A={H:{},I:{},P:None,Q:None};D={H:{E:path_test},I:{E:path_ref}}
		for(K,F)in D.items():
			if not F.get(E)or not os.path.exists(F[E]):A[J]=f"file {K} does not exist";return A
		R=FileReader(B.context.working_dir,B.context.config.file_reader,B.context.config.readers,config_alternate_path=B.context.origin_working_dir)
		for(K,F)in D.items():D[K][M]=R.read(F[E])
		C=D[H][M];G=D[I][M]
		if not C or not G:A['skipped']=True;return A
		A[H]=C.info();A[I]=G.info()
		if C.read_error:A[J]=C.read_error;return A
		L=CompareErrors(B.context.config.compare.errors_limit,B.context.config.compare.ignore_warnings);N,S=C.compare(CompareFloats(L,B.context.config.compare.float_thresholds),G,param_is_ref=True);A[P]=S;A[Q]=L.get_data()
		if N:A[J]=N;return A
		C.close();G.close();O=len(L.errors[SEVERITY_ERROR])
		if O>0:T=f"{O} comparison errors";A[J]=T
		return A
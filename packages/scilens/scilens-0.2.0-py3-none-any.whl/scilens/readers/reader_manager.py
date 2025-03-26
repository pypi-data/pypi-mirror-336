import os,sys
from importlib.metadata import entry_points
from scilens.readers.exceptions import NoReaderFound
from scilens.readers.reader_interface import ReaderOrigin
def extension_format(extension):
	A=extension
	if A.startswith('.'):A=A[1:]
	return A.upper()
from scilens.readers.reader_txt import ReaderTxt
from scilens.readers.reader_csv import ReaderCsv
from scilens.readers.reader_txt_fixed_cols import ReaderTxtFixedCols
BUILTIN_PLUGINS=[ReaderTxt,ReaderCsv,ReaderTxtFixedCols]
LIB_PLUGINS_ENTRY_POINT='scilens.reader_plugins'
class ReaderManager:
	def __init__(A):
		A.plugins=[]+BUILTIN_PLUGINS;B=entry_points(group=LIB_PLUGINS_ENTRY_POINT)if sys.version_info.minor>=12 else entry_points().get(LIB_PLUGINS_ENTRY_POINT,[])
		for C in B:A.plugins+=C.load()()
	def _get_plugin_names(A):return[A.__name__ for A in A.plugins]
	def __str__(A):return f"plugins: {A._get_plugin_names()}"
	def _get_reader_from_extension(B,extension):
		for A in B.plugins:
			if extension_format(extension)in A.extensions:return A
	def get_reader_from_file(D,path,name='',encoding='',curve_parser=None,extension_mapping=None,extension_fallback=None):
		F=extension_fallback;E=extension_mapping;C=path;J,A=os.path.splitext(C);A=extension_format(A)
		if E:
			for(G,H)in E.items():
				if extension_format(G)==A:A=extension_format(H);break
		B=D._get_reader_from_extension(A)
		if not B and F:B=D._get_reader_from_extension(F)
		if not B:raise NoReaderFound(f"Reader cound not be derived")
		I=ReaderOrigin(type='file',path=C,short_name=os.path.basename(C));return B(I,name=name,encoding=encoding,curve_parser=curve_parser)
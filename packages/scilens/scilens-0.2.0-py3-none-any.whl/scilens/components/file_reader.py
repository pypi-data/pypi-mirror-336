_A=None
import logging,importlib,os
from scilens.config.models import FileReaderConfig
from scilens.config.models.readers import ReadersConfig
from scilens.readers.reader_manager import ReaderManager
from scilens.readers.exceptions import NoReaderFound
class FileReader:
	def __init__(A,absolute_working_dir,config,readers_config,config_alternate_path=_A):A.path=absolute_working_dir;A.config_alternate_path=config_alternate_path;A.reader_mgmr=ReaderManager();A.config=config;A.readers_config=readers_config
	def _get_custom_parser(D,config_parser):
		E=config_parser
		if not E:return
		A,H=E.split('::');B=_A;I=[A,f"{D.path}/{A}",f"{D.config_alternate_path}/{A}"]
		for C in I:
			if os.path.exists(C):B=C;break
		if not B:raise Exception(f"Custom curve parser not found: {A}")
		J=C.split('/')[-1].replace('.py','');F=importlib.util.spec_from_file_location(J,B);G=importlib.util.module_from_spec(F);F.loader.exec_module(G);return getattr(G,H)
	def read(A,path):
		logging.info(f"Reading file: {path}");E=_A;D=A.config.custom_curve_parser
		if D:
			if isinstance(D,str):E=A._get_custom_parser(D)
		try:
			B=A.reader_mgmr.get_reader_from_file(path,encoding=A.config.encoding,curve_parser=E,extension_mapping=A.config.extension_mapping,extension_fallback=A.config.extension_fallback);C=_A
			if B.__class__.__name__=='ReaderTxt':C=A.readers_config.txt
			elif B.__class__.__name__=='ReaderCsv':C=A.readers_config.csv
			elif B.__class__.__name__=='ReaderTxtFixedCols':C=A.readers_config.txt_fixed_cols
			elif B.__class__.__name__=='ReaderNetcdf':C=A.readers_config.netcdf
			B.read(C)
		except NoReaderFound:
			if A.config.extension_unknown_ignore:0
			else:raise Exception(f"No reader found")
		return B
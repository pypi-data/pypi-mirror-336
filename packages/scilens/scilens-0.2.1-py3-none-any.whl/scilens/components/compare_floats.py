_B='amplitude'
_A=None
from scilens.components.compare_errors import CompareErrors,SEVERITY_ERROR,SEVERITY_WARNING,CompareErrFloats
from scilens.config.models import CompareFloatThresholdsConfig
try:from scilens_compare import vectors as CheckVectors
except ModuleNotFoundError:pass
def vector_get_amplitude(vector):min_val=min(vector);max_val=max(vector);return{'min':min_val,'max':max_val,_B:abs(max_val-min_val)}
class CompareFloats:
	def __init__(self,compare_errors,config):self.compare_errors=compare_errors;self.thresholds=config
	def compare_vectors(self,test_vector,reference_vector,group_idx=_A,info_vector=_A):
		A='ignore';diffs_count=0;counts={SEVERITY_ERROR:0,SEVERITY_WARNING:0};err_limit_reached=False;amplitude_compare=_A
		if self.thresholds.vectors and self.thresholds.vectors.ponderation_method=='amplitude_moderation':amplitude=vector_get_amplitude(test_vector)[_B];amplitude_compare=amplitude*self.thresholds.vectors.amplitude_moderation_multiplier;reduction_method=self.thresholds.vectors.reduction_method
		RIAE_force_severity=_A
		if self.thresholds.vectors and self.thresholds.vectors.ponderation_method in['RIAE','RIAE_trapezoid','RIAE_midpoint']:
			RIAE_force_severity=self.thresholds.vectors.reduction_method
			if'CheckVectors'not in globals():raise Exception('scilens_compare not found. Please install scilens-compare package with `pip install scilens-compare`.')
			riae_error=CheckVectors.relative_integral_absolute_error_trapezoid(reference_vector,test_vector,range(len(test_vector)));riae_error=CheckVectors.relative_integral_absolute_error_midpoint(reference_vector,test_vector,range(len(test_vector)));print('riae_error');print(riae_error)
			if riae_error<self.thresholds.vectors.riae_threshold:RIAE_force_severity=self.thresholds.vectors.reduction_method
			else:0
		nb=len(test_vector)
		for idx in range(nb):
			diff=test_vector[idx]-reference_vector[idx]
			if diff==0:continue
			else:diffs_count+=1
			if err_limit_reached:continue
			if RIAE_force_severity==A:continue
			if amplitude_compare is not _A and abs(diff)<amplitude_compare:
				if reduction_method==A:continue
				elif reduction_method=='soften':severity,message,comp_err=self.compare_2_values(test_vector[idx],reference_vector[idx]);severity=SEVERITY_WARNING
			else:
				severity,message,comp_err=self.compare_2_values(test_vector[idx],reference_vector[idx])
				if RIAE_force_severity:severity=SEVERITY_WARNING
			if comp_err:
				counts[severity]+=1;info={'index':idx}
				if info_vector:info['info']=info_vector[idx]
				err_limit_reached=self.compare_errors.add(severity,message,comp_err,group_idx=group_idx,info=info)
		return err_limit_reached,diffs_count,counts
	def compare_2_values(self,test,reference):
		thr=self.thresholds;sign=-1 if test-reference<0 else 1
		if abs(test)>thr.relative_vs_absolute_min and reference!=0:
			err=abs(test-reference)/abs(reference);comp_err=CompareErrFloats(is_relative=True,value=sign*err,test=test,reference=reference)
			if err<thr.relative_error_max:
				if err>thr.relative_error_min:return SEVERITY_WARNING,f"Rel. err. > {thr.relative_error_min} and < {thr.relative_error_max}",comp_err
			else:return SEVERITY_ERROR,f"Rel. err. > {thr.relative_error_max}",comp_err
		else:
			err=abs(test-reference);comp_err=CompareErrFloats(is_relative=False,value=sign*err,test=test,reference=reference)
			if err<thr.absolute_error_max:
				if err>thr.absolute_error_min:return SEVERITY_WARNING,f"Abs. err. > {thr.absolute_error_min} and < {thr.absolute_error_max}",comp_err
			else:return SEVERITY_ERROR,f"Abs. err. > {thr.absolute_error_max}",comp_err
		return _A,_A,_A
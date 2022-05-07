
from pathlib import Path
from pandas import date_range
from datetime import datetime as dtm
from datetime import timedelta as dtmdt
import pickle as pkl


# parents class for write out the data
# support csv, excel, pickle
class _writter:
	
	nam = None

	def __init__(self,path=None,start=None,end=None,parallel=False,
				 csv=True,excel=False,pickle=False):

		## default parameter
		path  = path  or Path('.')
		start = start or (dtm.now()-dtmdt(days=2)).strftime('%Y-%m-%d')
		end	  = end   or (dtm.now()-dtmdt(days=1)).strftime('%Y-%m-%d')

		## class parameter
		self.parallel = parallel
		self.dl_index = date_range(start,end,freq='1d')
		self.tm_index = date_range(self.dl_index[0],self.dl_index[-1]+dtmdt(days=1),
								   closed='left',freq='1h')

		## output parameter
		self.path	= path
		self.csv	= csv
		self.excel	= excel
		self.pickle	= pickle

		## meta information
		self._update_info_path = Path('AtmosDataCrawler')/'core'/'utils'/self.nam
		with (Path(__file__).parent/'utils'/self.nam/'info.pkl').open('rb') as f:
			self.info = pkl.load(f)

	## write out data
	def _save_out(self,_df_out):

		_st, _ed = self.dl_index.strftime('%Y%m%d')[[0,-1]]
		_out_nam = f"{self.nam}_{_st}_{_ed}"

		if self.csv:
			print(f'save : {_out_nam}.csv')
			_df_out.to_csv(self.path/f'{_out_nam}.csv')

		if self.excel:
			print(f'save : {_out_nam}.xlsx')
			from pandas import ExcelWriter
			with ExcelWriter(self.path/f'{_out_nam}.xlsx') as f:
				_df_out.to_excel(f,sheet_name=self.nam)

		if self.pickle:
			print(f'save : {_out_nam}.pkl')
			with (self.path/f'{_out_nam}.pkl').open('wb') as f:
				pkl.dump(_df_out,f,protocol=pkl.HIGHEST_PROTOCOL)

	## update information file in utils
	def __update_info(self,):
		pass
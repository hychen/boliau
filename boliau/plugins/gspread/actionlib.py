import gspread

from boliau import actionlib

class GspreaCleint(object):

    conn = None
    cur_spread = None
    
    def connect(self,  email,  password):
        if not self.conn:
            self.conn = gspread.login(email, password)

    def upsert_cells(self, data, spreadname, wksname='sheet1'):
        spread = self.conn.open(spreadname)

        if not spread:
            return "can not find spreadsheet {0}".format(spreadname)        

        try:            
            wks =  getattr(spread, wksname)
        except AttributeError:
            return "can not find worksheet {0}".format(wks)
            
        if type(data) is list:
            for row_i, row_v in enumerate(data):                
                for col_i, col_v in enumerate(row_v):                
                    wks.update_cell(row_i +1, col_i+1, col_v)
            return "done!"
        else:
            return "type of data should be list or dict. "

class _StreamAction(actionlib.StreamAction):

    def __init__(self):
        self.client =  GspreaCleint()
        super(_StreamAction, self).__init__()
 
class Upsert(_StreamAction):

    desc = """Insert or update google spread sheet cells"""

    link_type =  "Mission -> None"

    data_type = 'List -> Any'

    def __call__(self,  acc,  **opts):
        spreadsheet = opts['spreadsheet']
        wks = opts['worksheet']
        email = opts['email']
        password = opts['password']
        self.client.connect(email, password)
        data = acc()
        if data:
            return self.client.upsert_cells(data, spreadsheet,  wks)
        return "Can not insert.  data is None. "

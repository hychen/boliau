from boliau import actionlib
from boliau import util

class PyObj(object):

    desc = """Create a Python object"""

    link_type = "None -> Mission"

    data_type =  "None -> Any"

    def __init__(self):
        self.acc = actionlib.Mission()
    
    def __call__(self, **opts):
        self.acc.add_task(repr(self.__class__),
                          self.maintask,
                          **opts)
        return self.acc

    def maintask(db, **opts):
        if 'from_yaml' in opts:
            raise NotImplemented
        elif 'from_json' in opts:
            raise NotImplemented
        elif 'from_string' in opts:
            #@FIXME: can not curry imported module to next mission.
            import json
            obj = json.loads(opts['from_string'])
        return obj

class PyCall(actionlib.StreamAction):

    desc = """
    Call Python function
    """

    link_type = 'Mission -> Mission'
    
    data_type = 'Any -> Any'

    def __call__(self, acc, **opts):
        query = opts.pop('func')
        try:
            fn = util.import_mod_fn(query)
        except Exception as e:
            raise actionlib.BadMissionMessage("PyCall: {0}".format(e))
        acc.add_task(query, fn, **opts)
        return acc

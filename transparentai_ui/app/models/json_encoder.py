from sqlalchemy.ext.declarative import DeclarativeMeta
import json

class JSONEncoder(json.JSONEncoder):
    """
    https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json
    """

    def default(self, obj):
        

        return str(obj)
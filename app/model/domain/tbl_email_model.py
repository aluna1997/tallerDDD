from datetime import date
from sqlalchemy.sql.sqltypes import Date

class TblEmailModel:
    def __init__(self):
        self.IdEmail: int
        self.Email: str
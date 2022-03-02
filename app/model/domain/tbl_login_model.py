from sqlalchemy.sql.sqltypes import DateTime

class TblLoginModel:
    def __init__(self):
        self.IdLogin: int
        self.IdEmail: int
        self.Codigo: str
        self.FechaAcceso: DateTime
        self.VecesLogin: int
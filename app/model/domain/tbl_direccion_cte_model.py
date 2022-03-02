from datetime import date
from sqlalchemy.sql.sqltypes import Date

class TblDireccionClienteModel:
    def __init__(self):
        self.IdDireccion: int
        self.IdCliente: int
        self.Calle: str
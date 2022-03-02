from datetime import date
from sqlalchemy.sql.sqltypes import Date

class TblClienteModel:
    def __init__(self):
        self.IdCliente: int
        self.NumCte: str
        self.Email: str
        self.PrimerNombre: str
        self.SegundoNombre: str
        self.ApPaterno: str
        self.CURP: str
        self.FechaNac: Date
        self.Celular: str
        self.RFC: str

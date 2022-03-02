from datetime import date
from sqlalchemy.sql.sqltypes import Date

class TblProspectoModel:
    def __init__(self):
        self.IdProspecto: int
        self.IdEmail: int
        self.IdEstatusSol: int
        self.PrimerNombre: str
        self.SegundoNombre: str
        self.ApPaterno: str
        self.ApMaterno: str
        self.CURP: str
        self.FechaNac: Date
        self.RFC: str
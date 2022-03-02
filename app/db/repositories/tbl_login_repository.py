import imp
from typing import Any
from common.db.base import BaseRepository
from model.domain.tbl_login_model import TblLoginModel

class TblLoginRepository(BaseRepository):
    def __init__(self, session) -> None:
        super().__init__()
        self.session = session

    def get(self, id: int) -> Any:
        return self.session.query(TblLoginModel).filter_by(Id=id).first()
        
    def add(self, tbl_login_model):
        self.session.add(tbl_login_model)  

    def obtener_codigo(self,codigo: str,id_email: int) -> Any:
        return self.session.query(TblLoginModel).filter_by(Codigo = codigo,IdEmail = id_email).first()


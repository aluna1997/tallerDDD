import imp
from typing import Any
from common.db.base import BaseRepository
from model.domain.tbl_direccion_cte_model import TblDireccionClienteModel

class CatEstatusSolRepository(BaseRepository):
    def __init__(self, session) -> None:
        super().__init__()
        self.session = session

    def get(self, id: int) -> Any:
        return self.session.query(TblDireccionClienteModel).filter_by(Id=id).first()
        
    def add(self, tbl_direccion_cte_model):
        self.session.add(tbl_direccion_cte_model)      


from typing import Any
from common.db.base import BaseRepository
from model.domain.tbl_celular_model import TblCelularModel

class CatEstatusSolRepository(BaseRepository):
    def __init__(self, session) -> None:
        super().__init__()
        self.session = session

    def get(self, id: int) -> Any:
        return self.session.query(TblCelularModel).filter_by(Id=id).first()
        
    def add(self, tbl_celular_model):
        self.session.add(tbl_celular_model)      


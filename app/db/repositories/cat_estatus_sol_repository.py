from typing import Any
from common.db.base import BaseRepository
from model.domain.cat_estatus_sol_model import CatEstatusSolModel

class CatEstatusSolRepository(BaseRepository):
    def __init__(self, session) -> None:
        super().__init__()
        self.session = session

    def get(self, id: int) -> Any:
        return self.session.query(CatEstatusSolModel).filter_by(Id=id).first()
        
    def add(self, cat_estatus_sol_model):
        self.session.add(cat_estatus_sol_model)      


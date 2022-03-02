import imp
from typing import Any
from common.db.base import BaseRepository
from model.domain.tbl_email_model import TblEmailModel

class EmailRepository(BaseRepository):
    def __init__(self, session) -> None:
        super().__init__()
        self.session = session

    def get(self, id: int) -> Any:
        return self.session.query(TblEmailModel).filter_by(Id=id).first()
        
    def add(self, tbl_email_model):
        self.session.add(tbl_email_model) 
        self.session.flush()
        self.session.refresh(tbl_email_model) 

    def obtener_id_email(self, email):
        return self.session.query(TblEmailModel).filter_by(Email=email).first()


import re
from fastapi import Request
from services.constants import REGEX_EMAIL
from model.errors import EmailInvalidoException
from loguru import logger
from fastapi import HTTPException

class EmailValidator:
    
    def __init__(self, param_name:str = None):
        '''
        Inicializa el validador
        @param_name: es el nombre del parámetro que viene en la ruta
        '''
        self.param_name:str = param_name
    
    def __call__(self, request:Request):
        '''
        Se validara que el correo contenga un formato de correo electronico valido
        @request:Obtiene el valor del parametro.
        '''
        try:
            req_correo = str(request.path_params[self.param_name])
            
            if re.fullmatch(REGEX_EMAIL,req_correo):
                logger.info("El correo es valido ")
            else:    
                raise EmailInvalidoException(description="El correo {} no tiene formato valido".format(req_correo))            
            
        except EmailInvalidoException as exc:
            logger.exception(exc)
            raise HTTPException(
                status_code = 404,
                detail = str(exc),
                headers={"WWW-Authenticate": "Bearer"},
            )
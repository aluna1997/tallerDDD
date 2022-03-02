import pdb
import re
from random import choice
from operator import ne
from typing import Any

from sqlalchemy.sql.sqltypes import Date
from db.demo_uow import SqlAlchemyUnitOfWork

from datetime import date, datetime
from model.domain.base_model import BaseModel

import requests
from loguru import logger
from model.errors import EmailInvalidoException, EntityNotFoundException
from starlette import status
from fastapi import HTTPException


from model.rest import TestData, TestResponse
from db.demo_uow import ProspectoUnitOfWork
from db.demo_uow import CodigoUnitOfWork
from db.repositories.tbl_email_repository import TblEmailModel
from db.repositories.tbl_prospecto_repository import TblProspectoModel
from model.rest import NuevoProspectoRequest
from model.rest import LoginRequest
from model.domain.tbl_login_model import TblLoginModel

HTTP_SESSION = requests.Session()
SOLICITUD_EN_PROCESO = 1

def probar_http_session(token: str, num_cta:str) -> TestResponse:
    head = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}
    req = requests.Request('GET',  f"https://apim.perfekti.mx/v1/cuentas/{num_cta}/saldos/",
        headers=head
    )
    prepped = HTTP_SESSION.prepare_request(req)
    resp = HTTP_SESSION.send(prepped)

    response = TestResponse(
        estatus = resp.status_code,
        mensaje = "OK",
        datos = TestData(
            valor1 = 1,
            valor2 = "Nada"
        ),
    )
    return response

def agregar_registro(nombre: str, mensaje: str)->int:
    with SqlAlchemyUnitOfWork() as uow:
        new_model = BaseModel()
        new_model.FechaReporte = date.today()
        new_model.CodigoClave = 2
        new_model.TipoInstitucion = nombre
        new_model.Mensaje = mensaje
        new_model.FacebookId  = "10154509875362000"
        new_model.Respuesta = 23
        uow.base_repository.add(new_model)
        uow.commit()
    return new_model.Id

def obtener_registro(id: int) -> BaseModel:
    with SqlAlchemyUnitOfWork() as uow:
        return uow.base_repository.get(id)

def consulta_retenido() -> Any:
    with SqlAlchemyUnitOfWork() as uow:
        return uow.base_repository.obtener_suma_movimientos_pendientes(89596)

def consulta_retenido_amex() -> Any:
    with SqlAlchemyUnitOfWork() as uow:
        return uow.base_repository.obtener_suma_movimientos_pendientes_amex(89596)


def registrar_nuevo_prospecto_model(data: NuevoProspectoRequest) -> Any:
    try:
        with ProspectoUnitOfWork() as uow:
            email = TblEmailModel()
            email.Email = data.email
            uow.email_repository.add(email)

            prospecto = TblProspectoModel()
            prospecto.IdEmail = email.IdEmail
            prospecto.IdEstatusSol = SOLICITUD_EN_PROCESO
            prospecto.PrimerNombre = data.primerNombre
            prospecto.SegundoNombre = data.segundoNombre
            prospecto.ApPaterno = data.apPaterno
            prospecto.ApMaterno = data.apMaterno
            prospecto.CURP = data.curp
            prospecto.FechaNac = data.fechaNac
            prospecto.RFC = data.rfc

            
            uow.prospecto_repository.add(prospecto)
            uow.commit()

            return email.IdEmail,prospecto.IdProspecto
    except Exception as exc:
        logger.exception(exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        )

def genera_codigo_email(email: str) -> str:
    try:
        with CodigoUnitOfWork() as uow:
            expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
            correo_valido = re.match(expresion_regular, email) is not None

            if not correo_valido:
                raise EmailInvalidoException("El email no esta bien formado")

            id_email = uow.email_repository.obtener_id_email(email)

            if not id_email:
                raise EntityNotFoundException("No existe ese email")

            longitud = 4
            valores = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ<=>@#%&+"

            codigo = ""
            codigo = codigo.join([choice(valores) for i in range(longitud)])

            login = TblLoginModel()
            login.Codigo = codigo
            login.IdEmail = id_email.IdEmail
            
            uow.login_repository.add(login)
            uow.commit()

            return codigo
    
    except EmailInvalidoException as exc:
        logger.exception(exc)
        raise HTTPException(
            status_code = 422,
            detail = str(exc),
            headers = {"WWW-Authenticate": "Bearer"},
        )
    except EntityNotFoundException as exc:
        logger.exception(exc)
        raise HTTPException(
            status_code = 404,
            detail = str(exc),
            headers = {"WWW-Authenticate": "Bearer"},
        )
    except Exception as exc:
        logger.exception(exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        )

def login_email_model(data: LoginRequest) -> Any:
    try:
        with CodigoUnitOfWork() as uow:
            email_obj = uow.email_repository.obtener_id_email(data.email)
            if not email_obj:
                raise EntityNotFoundException

            codigo_obj = uow.login_repository.obtener_codigo(data.codigo,email_obj.IdEmail)
            if not codigo_obj:
                raise EntityNotFoundException
            
            codigo_obj.FechaAcceso = datetime.now()
            codigo_obj.VecesLogin += 1

            uow.login_repository.add(codigo_obj)
            uow.commit()

    except EntityNotFoundException as exc:
        logger.exception(exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        )

    except Exception as exc:
        logger.exception(exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        )

from pydantic import BaseModel
from typing import Optional
from datetime import date,datetime

################################################################################
### Clases que se reciben
################################################################################

class TestRequest(BaseModel):
    primer_campo: str
    segundo_campo: str
    tercer_campo: Optional[str] = None

class DatosAlta(BaseModel):
    nombre:str
    comentarios:str

################################################################################
### Clases que se envían
################################################################################

class TestData(BaseModel):
    valor1: int
    valor2: str

class TestResponse(BaseModel):
    estatus: int
    mensaje: str
    datos: TestData

class NuevoProspectoRequest(BaseModel):
    email: str
    primerNombre: str
    segundoNombre: str
    apPaterno: str
    apMaterno: str
    curp: str
    fechaNac: date
    rfc: str



class NuevoProspectoResponse(BaseModel):
    idEmail: int
    idProspecto: int
    status: int
    mensaje: str

#### CODIGO EMAIL ####
class CodigoResponse(BaseModel):
    status: int
    mensaje: str
    codigo: str

#### LOGIN ####
class LoginRequest(BaseModel):
    email: str
    codigo: str

class LoginResponse(BaseModel):
    estatus: int
    mensaje: str

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date,datetime
from services.constants import REGEX_EMAIL

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
    email: Optional[str] = Field(None, title="email", description="El email del usuario que quiere ingresar al APP")
    codigo: Optional[str] = Field(None, title="codigo",description="El código que el usuario generó para ingresar al APP")

class LoginResponse(BaseModel):
    estatus: int
    mensaje: str

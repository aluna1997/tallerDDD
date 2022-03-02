from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    String,
    Date,
    null,
)
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.sql.expression import false
from model.domain.base_model import BaseModel
from model.domain.cat_estatus_sol_model import CatEstatusSolModel
from model.domain.tbl_celular_model import TblCelularModel
from model.domain.tbl_cliente_model import TblClienteModel
from model.domain.tbl_direccion_cte_model import TblDireccionClienteModel
from model.domain.tbl_direccion_sol_model import TblDireccionSolModel
from model.domain.tbl_prospecto_model import TblProspectoModel
from model.domain.tbl_email_model import TblEmailModel
from model.domain.tbl_login_model import TblLoginModel
from model.domain.tbl_prospecto_model import TblProspectoModel

metadata = MetaData()
################################################################################
### Se debe de realizar el mapeo entre clases de negocio y la base de datos
### el mapeo se hace del modo "tradicional" de SQLAlquemy
################################################################################
tabla_ejemplo = Table(
    "tbc_hawk_alert",
    metadata,
    Column("idHawkAlert", Integer, primary_key=True, autoincrement=True),
    Column("C_FechaReporte", Date, nullable=True),
    Column("C_CodigoClave", Integer, nullable=True),
    Column("C_TipoInstitucion", String(45), nullable=True),
    Column("C_Mensaje", String(60), nullable=True),
    Column("BD_CodigoClave", Integer, nullable=True),
    Column("BD_TipoInstitucion", String(45), nullable=True),
    Column("BD_Mensaje", String(60), nullable=True),
    Column("fbid", String(20), nullable=False),
    Column("idRespuesta", Integer, nullable=True),
)

tbl_email = Table(
    "tbl_email",
    metadata,
    Column("id_email", Integer, primary_key=True, autoincrement=True, nullable=False),
    Column("email", String(50), nullable=False, unique=True)
)

tbl_cat_estatus_sol = Table(
    "cat_estatus_sol",
    metadata,
    Column("id_estatus", Integer, primary_key=True, autoincrement=True, nullable=False),
    Column("estatus", String(50), nullable=False, unique=True)
)

tbl_login = Table(
    "tbl_login",
    metadata,
    Column("id_login", Integer, primary_key=True, autoincrement=True, nullable=False),
    Column("id_email", Integer, nullable=False),
    Column("codigo", String(4), nullable=True),
    Column("fecha_acceso", Date, nullable=True),
    Column("veces_login", Integer, nullable=False),
)

tbl_prospecto = Table(
    "tbl_prospecto",
    metadata,
    Column("id_prospecto", Integer, primary_key=True, autoincrement=True, nullable=False),
    Column("id_email", Integer, nullable=False),
    Column("id_estatus_sol", Integer, default=null),
    Column("primer_nombre", String(30), nullable=False),
    Column("segundo_nombre", String(30), default=null),
    Column("ap_paterno", String(50), nullable=False),
    Column("ap_materno", String(50)),
    Column("CURP", String(20), nullable=False),
    Column("fecha_nac", Date, default=null),
    Column("RFC", String(20), nullable=False)
)

tbl_direccion_sol = Table(
    "tbl_direccion_sol",
    metadata,
    Column("id_direccion", Integer, primary_key=True, autoincrement=True, nullable=False),
    Column("id_sol", Integer, nullable=False),
    Column("calle", String(50), nullable=False, unique=True)
)

tbl_celular = Table(
    "tbl_celular",
    metadata,
    Column("id_tel", Integer, primary_key=True, autoincrement=True, nullable=False),
    Column("tel", String(5), nullable=False, unique=True),
    Column("id_sol", Integer, nullable=False)
)

tbl_cliente = Table(
    "tbl_cliente",
    metadata,
    Column("id_cliente", Integer, primary_key=True, autoincrement=True, nullable=False),
    Column("num_cte", String(30), nullable=False),
    Column("email", String(50), nullable=False),
    Column("primer_nombre", String(30), nullable=False),
    Column("segundo_nombre", String(30)),
    Column("ap_paterno", String(50), nullable=False),
    Column("ap_materno", String(50)),
    Column("CURP", String(20), nullable=False),
    Column("fecha_nac", Date, default=null),
    Column("celular", String(20), nullable=False),
    Column("RFC", String(20), nullable=False)
)

tbl_direccion_cte = Table(
    "tbl_direccion_cte",
    metadata,
    Column("id_direccion", Integer, primary_key=True, autoincrement=True, nullable=False),
    Column("id_cliente", Integer),
    Column("calle", String(50), nullable=False, unique=True)
)

################################################################################
### Este método se llama al inicio del programa, no se debe de cambiar el
### nombre de la función y debe de contener todos los mapeos
################################################################################
def start_mappers():
    mapper(BaseModel, tabla_ejemplo, properties={
        'Id': tabla_ejemplo.c.idHawkAlert,
        'FechaReporte': tabla_ejemplo.c.C_FechaReporte,
        'CodigoClave': tabla_ejemplo.c.C_CodigoClave,
        'TipoInstitucion': tabla_ejemplo.c.C_TipoInstitucion,
        'Mensaje': tabla_ejemplo.c.C_Mensaje,
        'FacebookId': tabla_ejemplo.c.fbid,
        'Respuesta': tabla_ejemplo.c.idRespuesta,
    })

    mapper(TblEmailModel, tbl_email, properties={
        'IdEmail': tbl_email.c.id_email,
        'Email': tbl_email.c.email
    })

    mapper(CatEstatusSolModel, tbl_cat_estatus_sol, properties={
        'IdEstatus': tbl_cat_estatus_sol.c.id_estatus,
        'Estatus': tbl_cat_estatus_sol.c.estatus
    })

    mapper(TblLoginModel, tbl_login, properties={
        'IdLogin': tbl_login.c.id_login,
        'IdEmail': tbl_login.c.id_email,
        'Codigo': tbl_login.c.codigo,
        'FechaAcceso': tbl_login.c.fecha_acceso,
        'VecesLogin': tbl_login.c.veces_login
    })

    mapper(TblProspectoModel, tbl_prospecto, properties={
        'IdProspecto': tbl_prospecto.c.id_prospecto,
        'IdEmail': tbl_prospecto.c.id_email,
        'IdEstatusSolicitud': tbl_prospecto.c.id_estatus_sol,
        'PrimerNombre': tbl_prospecto.c.primer_nombre,
        'SegundoNombre': tbl_prospecto.c.segundo_nombre,
        'ApellidoPaterno': tbl_prospecto.c.ap_paterno,
        'ApellidoMaterno': tbl_prospecto.c.ap_materno,
        'CURP': tbl_prospecto.c.CURP,
        'FechaNacimiento': tbl_prospecto.c.fecha_nac,
        'RFC': tbl_prospecto.c.RFC,
    })

    mapper(TblDireccionSolModel, tbl_direccion_sol, properties={
        'IdDireccion': tbl_direccion_sol.c.id_direccion,
        'IdSolicitud': tbl_direccion_sol.c.id_sol,
        'Calle': tbl_direccion_sol.c.calle
    })

    mapper(TblCelularModel, tbl_celular, properties={
        'IdTelefono': tbl_celular.c.id_tel,
        'Telefono': tbl_celular.c.tel,
        'IdSolicitud': tbl_celular.c.id_sol
    })

    mapper(TblClienteModel, tbl_cliente, properties={
        'IdCliente': tbl_cliente.c.id_cliente,
        'NumeroCliente': tbl_cliente.c.num_cte,
        'Email': tbl_cliente.c.email,
        'PrimerNombre': tbl_cliente.c.primer_nombre,
        'SegundoNombre': tbl_cliente.c.segundo_nombre,
        'ApellidoPaterno': tbl_cliente.c.ap_paterno,
        'ApellidoMaterno': tbl_cliente.c.ap_materno,
        'CURP': tbl_cliente.c.CURP,
        'FechaNacimiento': tbl_cliente.c.fecha_nac,
        'Celular': tbl_cliente.c.celular,
        'RFC': tbl_cliente.c.RFC,
    })

    mapper(TblDireccionClienteModel, tbl_direccion_cte, properties={
        'IdDireccion': tbl_direccion_cte.c.id_direccion,
        'IdCliente': tbl_direccion_cte.c.id_cliente,
        'Calle': tbl_direccion_cte.c.calle
    })
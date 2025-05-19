from pydantic import BaseModel, ConfigDict, EmailStr

from yawara.models import Tipo


class Token(BaseModel):
    access_token: str
    token_type: str

class Message(BaseModel):
    message: str

class UsuarioFuncionarioSchema(BaseModel):
    login: str
    senha: str
    nome: str
    cpf: str
    email: EmailStr
    tipo: Tipo


class UsuarioFuncionarioPublic(BaseModel):
    id: int
    nome: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)
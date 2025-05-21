from typing import List

from pydantic import BaseModel, ConfigDict, EmailStr

from yawara.models import Tipo


class Token(BaseModel):
    access_token: str
    token_type: str


class Message(BaseModel):
    message: str


class UsuarioBase(BaseModel):
    login: str

    class Config:
        orm_mode = True

class FuncionarioBase(BaseModel):
    id: int
    nome: str
    cpf: str
    email: str
    tipo: Tipo
    usuario: UsuarioBase  # Aqui acessamos apenas o login

    class Config:
        orm_mode = True


class PetSchema(BaseModel):
    dono: int
    nome: str


class PetBase(BaseModel):
    id: int
    nome: str
    class Config:
        orm_mode = True



class ServicoBase(BaseModel):
    pet_id: int
    cliente_id: int
    descricao: str

class ServicoResponse(BaseModel):
    id: int
    descricao: str
    cliente_id: int
    funcionario_id: int
    pet_id: int

    class Config:
        orm_mode = True


class PetResponse(PetSchema):
    id: int


class PetList(BaseModel):
    pets: list[PetResponse]


class ClienteBase(BaseModel):
    id: int
    nome: str
    cpf: str
    email: str
    telefone: str
    usuario: UsuarioBase  # Aqui acessamos apenas o login

class ClienteBaseComPets(BaseModel):
    id: int
    nome: str
    cpf: str
    email: str
    telefone: str
    usuario: UsuarioBase  # Aqui acessamos apenas o login
    pets: List[PetBase]
    class Config:
        orm_mode = True


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
    cpf: str
    email: EmailStr
    tipo: Tipo


class UsuarioFuncionarioList(BaseModel):
    usuarios: list[UsuarioFuncionarioPublic]


class PetsSchema(BaseModel):
    nome: str
    dono: int


class PetsList(BaseModel):
    pets: list[PetsSchema]


class UsuarioClienteSchema(BaseModel):
    login: str
    senha: str
    nome: str
    cpf: str
    email: EmailStr
    endereco: str
    telefone: str


class UsuarioClientePublic(BaseModel):
    id: int
    nome: str
    email: EmailStr
    pets: List[PetBase]
    model_config = ConfigDict(from_attributes=True)


class DonoBase(BaseModel):
    id: int
    nome: str

    class Config:
        orm_mode = True

class PetComDonoResponse(BaseModel):
    id: int
    nome: str
    cliente: DonoBase  # Aqui entra o objeto dono, com nome, etc.

    class Config:
        orm_mode = True

class PetListComDono(BaseModel):
    pets: List[PetComDonoResponse]

from datetime import datetime
from typing import List, Optional
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

class PetBase(BaseModel):
    id: int
    nome: str
    class Config:
        orm_mode = True

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





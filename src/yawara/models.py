from datetime import datetime
from sqlalchemy import ForeignKey, func
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()

class Tipo(str, Enum):
    normal = 'normal'
    adm = 'adm'

@table_registry.mapped_as_dataclass
class Usuario:
    __tablename__ = 'usuarios'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    login: Mapped[str] = mapped_column(unique=True)
    senha: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
      init=False,
      onupdate=func.now(),
      nullable=True,
      server_default=func.now(),
    )

@table_registry.mapped_as_dataclass
class Funcionario:
    __tablename__ = 'funcionarios'

    id: Mapped[int] = mapped_column(ForeignKey('usuarios.id'), init=True, primary_key=True)
    nome: Mapped[str] 
    cpf: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    tipo: Mapped[Tipo]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
      init=False,
      onupdate=func.now(),
      nullable=True,
      server_default=func.now(),
    )

class Cliente:
    __tablename__ = 'clientes'

    id: Mapped[int] = mapped_column(ForeignKey('usuarios.id'), init=True, primary_key=True)
    nome: Mapped[str] 
    cpf: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    endereco: Mapped[str]
    telefone: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
      init=False,
      onupdate=func.now(),
      nullable=True,
      server_default=func.now(),
    )

class Pet:
    __tablename__ = 'pets'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str] 
    dono: Mapped[str] = mapped_column(ForeignKey('clientes.id'))
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
      init=False,
      onupdate=func.now(),
      nullable=True,
      server_default=func.now(),
    )

class Servico:
    __tablename__ = 'servicos'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    cliente: Mapped[str] = mapped_column(ForeignKey('clientes.id'))
    funcionario: Mapped[str] = mapped_column(ForeignKey('funcionarios.id'))
    pet: Mapped[str] = mapped_column(ForeignKey('pets.id'))
    descricao: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
      init=False,
      onupdate=func.now(),
      nullable=True,
      server_default=func.now(),
    )

from datetime import datetime
from enum import Enum
from typing import List

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


class Tipo(str, Enum):
    normal = 'normal'
    adm = 'adm'

class Status(str, Enum):
    pendente = 'pendente'
    concluido = 'concluido'

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


##################################################################
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

    # Relacionamento reverso (um-para-um com Usuario)
    usuario: Mapped["Usuario"] = relationship(
        lazy="joined",
        init=False
    )

    servicos: Mapped["Servico"] = relationship(
        back_populates="funcionario",
        init=False
    )


@table_registry.mapped_as_dataclass
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

    # Relacionamento reverso (um-para-um com Usuario)
    usuario: Mapped["Usuario"] = relationship(
        lazy="joined",
        init=False
    )

     # 🔹 Relacionamento 1:N com Pet
    pets: Mapped[List["Pet"]] = relationship(
        back_populates="cliente",
        init=False
    )

    servicos: Mapped["Servico"] = relationship(
        back_populates="cliente",
        init=False
    )



@table_registry.mapped_as_dataclass
class Pet:
    __tablename__ = 'pets'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str]
    dono: Mapped[int] = mapped_column(ForeignKey('clientes.id'))
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
      init=False,
      onupdate=func.now(),
      nullable=True,
      server_default=func.now(),
    )

    # 🔹 Relacionamento reverso N:1 com Cliente
    cliente: Mapped["Cliente"] = relationship(
        back_populates="pets",
        init=False
    )

    servicos: Mapped["Servico"] = relationship(
        back_populates="pet",
        init=False
    )

@table_registry.mapped_as_dataclass
class Servico:
    __tablename__ = 'servicos'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey('clientes.id'))
    funcionario_id: Mapped[int] = mapped_column(ForeignKey('funcionarios.id'))
    pet_id: Mapped[int] = mapped_column(ForeignKey('pets.id'))
    descricao: Mapped[str]
    status: Mapped[Status]

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
      init=False,
      onupdate=func.now(),
      nullable=True,
      server_default=func.now(),
    )

    cliente: Mapped["Cliente"] = relationship(init=False)
    funcionario: Mapped["Funcionario"] = relationship(init=False)
    pet: Mapped["Pet"] = relationship(init=False)
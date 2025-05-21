
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from yawara.database import get_session
from yawara.models import Cliente, Funcionario, Usuario
from yawara.schemas import (
    ClienteBase,
    ClienteBaseComPets,
    FuncionarioBase,
    UsuarioClienteSchema,
    UsuarioFuncionarioSchema,
)
from yawara.security import get_current_user, get_password_hash

router = APIRouter(prefix='/usuarios', tags=['usuarios'])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[Usuario, Depends(get_current_user)]


@router.post('/funcionario', status_code=HTTPStatus.CREATED, response_model=FuncionarioBase)
def criar_usuario_funcionario(usuario: UsuarioFuncionarioSchema, session: T_Session):
    """Criar login de funcionario"""
    db_user = session.scalar(
        select(Usuario).where(
            (Usuario.login == usuario.login)
        )
    )

    if db_user:
        if db_user.login == usuario.login:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Login já existe'
            )

    hashed_password = get_password_hash(usuario.senha)

    db_user = Usuario(
        login=usuario.login,
        senha=hashed_password
    )

    session.add(db_user)
    session.flush()

    db_funcionario = Funcionario(
        id=db_user.id,
        nome=usuario.nome,
        cpf=usuario.cpf,
        email=usuario.email,
        tipo=usuario.tipo
    )

    session.add(db_funcionario)
    session.commit()
    session.refresh(db_funcionario)

    return db_funcionario


@router.post('/cliente', status_code=HTTPStatus.CREATED, response_model=ClienteBase)
def criar_usuario_cliente(usuario: UsuarioClienteSchema, session: T_Session):
    """Criar login de cliente"""
    db_user = session.scalar(
        select(Usuario).where(
            (Usuario.login == usuario.login)
        )
    )

    if db_user:
        if db_user.login == usuario.login:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Login já existe'
            )

    hashed_password = get_password_hash(usuario.senha)

    db_user = Usuario(
        login=usuario.login,
        senha=hashed_password
    )

    session.add(db_user)
    session.flush()

    db_cliente = Cliente(
        id=db_user.id,
        nome=usuario.nome,
        cpf=usuario.cpf,
        email=usuario.email,
        endereco=usuario.endereco,
        telefone=usuario.telefone
    )

    session.add(db_cliente)
    session.commit()
    session.refresh(db_cliente)

    return db_cliente


@router.get('/funcionario', status_code=HTTPStatus.OK)
def listar_usuarios_funcionario(session: T_Session):
    """Retorna todos os funcionários com seus respectivos logins"""
    funcionarios = session.scalars(
        select(Funcionario).options(joinedload(Funcionario.usuario))
    ).all()

    # Montar a resposta manualmente para incluir login do usuário
    resultado = []
    for f in funcionarios:
        resultado.append({
            "id": f.id,
            "nome": f.nome,
            "email": f.email,
            "cpf": f.cpf,
            "tipo": f.tipo,
            "login": f.usuario.login if f.usuario else None
        })

    return {"Funcionarios": resultado}


@router.get('/cliente', status_code=HTTPStatus.OK, response_model=dict[str, list[ClienteBaseComPets]])
def listar_usuarios_cliente(session: T_Session):
        """Retorna todos os clientes com seus respectivos logins e lista de pets cadastrados"""
        usuarios = session.scalars(select(Cliente)).all()
        return {'Clientes': usuarios}

@router.get('/funcionario/{funcionario_id}', status_code=HTTPStatus.OK, response_model=FuncionarioBase)
def listar_usuario_funcionario(funcionario_id: int, session: T_Session):
     funcionario = session.scalar(
          select(Funcionario).where(
               Funcionario.id == funcionario_id
          )
     )

     if not funcionario:
          raise HTTPException(
               status_code=HTTPStatus.BAD_REQUEST,
               detail='Funcionario não encontrado'
          )
     
     return funcionario

@router.get('/cliente/{cliente_id}', status_code=HTTPStatus.OK, response_model=ClienteBaseComPets)
def listar_usuario_cliente(cliente_id: int, session: T_Session):
        cliente = session.scalar(
            select(Cliente).where(
                Cliente.id == cliente_id
            )
        )

        if not cliente:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Cliente não encontrado'
            )

        return cliente

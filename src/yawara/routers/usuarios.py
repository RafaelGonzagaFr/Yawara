
from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from yawara.database import get_session
from yawara.models import Funcionario, Usuario
from yawara.schemas import UsuarioFuncionarioPublic, UsuarioFuncionarioSchema
from yawara.security import get_current_user, get_password_hash


router = APIRouter(prefix='/usuarios', tags=['usuarios'])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[Usuario, Depends(get_current_user)]

@router.post('/funcionario', status_code=HTTPStatus.CREATED, response_model=UsuarioFuncionarioPublic)
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
    session.commit()
    session.refresh(db_user)

    db_user = session.scalar(
        select(Usuario).where(
            (Usuario.login == usuario.login)
        )
    )

    db_funcionario = Funcionario(
        id = db_user.id,
        nome = usuario.nome,
        cpf = usuario.cpf,
        email = usuario.email,
        tipo = usuario.tipo
    )

    session.add(db_funcionario)
    session.commit()
    session.refresh(db_funcionario)

    return db_funcionario
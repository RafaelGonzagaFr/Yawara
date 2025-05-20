from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pytest import Session
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from yawara.database import get_session
from yawara.models import Cliente, Funcionario, Pet, Servico, Usuario
from yawara.schemas import ServicoBase, ServicoResponse
from yawara.security import get_current_user

router = APIRouter(prefix='/servicos', tags=['servicos'])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[Usuario, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.OK, response_model=ServicoResponse)
def criar_servico(current_user: T_CurrentUser, servico: ServicoBase, session: T_Session):
    db_user = session.scalar(
        select(Funcionario).where(
            (Funcionario.id == current_user.id)
        )
    )

    if db_user:
        db_cliente = session.scalar(
          select(Cliente).where(
            (Cliente.id == servico.cliente_id)
          )
        )

        if not db_cliente:
            raise HTTPException(
              status_code=HTTPStatus.BAD_REQUEST,
              detail='Esse cliente não existe'
            )

        db_pet = session.scalar(
            select(Pet).where(
              (Pet.id == servico.pet_id)
            )   
        )

        if not db_pet:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Esse pet não existe'
            )

        db_servico = Servico(
            cliente_id=servico.cliente_id,
            pet_id=servico.pet_id,
            funcionario_id=current_user.id,
            descricao=servico.descricao
        )

        session.add(db_servico)
        session.commit()
        session.refresh(db_servico)

        return db_servico
    
    raise HTTPException(
        status_code=HTTPStatus.BAD_REQUEST,
        detail='Usuário não autorizado'
    )

@router.get('/', status_code=HTTPStatus.OK, response_model=list[ServicoResponse])
def lista_servicos(session: T_Session):
    db_servico = db_servico = session.scalars(select(Servico)).all()
    
    return db_servico

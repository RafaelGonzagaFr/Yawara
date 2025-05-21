from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pytest import Session
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from yawara.database import get_session
from yawara.models import Cliente, Funcionario, Pet, Servico, Usuario
from yawara.schemas import ServicoBase, ServicoResponse, ServicoResponseGet
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
            descricao=servico.descricao,
            status="pendente"
        )

        session.add(db_servico)
        session.commit()
        session.refresh(db_servico)

        return db_servico
    
    raise HTTPException(
        status_code=HTTPStatus.BAD_REQUEST,
        detail='Usuário não autorizado'
    )

@router.get('/', status_code=HTTPStatus.OK, response_model=list[ServicoResponseGet])
def lista_servicos(session: T_Session):
    servicos = session.scalars(
        select(Servico)
        .options(
            joinedload(Servico.cliente),
            joinedload(Servico.funcionario),
            joinedload(Servico.pet)
        )
    ).all()

    resposta = [
        ServicoResponseGet(
            id=s.id,
            cliente_nome=s.cliente.nome,
            funcionario_nome=s.funcionario.nome,
            pet_nome=s.pet.nome,
            descricao=s.descricao,
            status=s.status,
            created_at=s.created_at,
            updated_at=s.updated_at
        )
        for s in servicos
    ]

    return resposta

@router.patch('/status/{servico_id}', status_code=HTTPStatus.OK, response_model=ServicoResponse)
def alterar_status_servico(servico_id: int, session: T_Session):
    """Mudar status do servico"""
    servico = session.scalar(
        select(Servico).where(
            Servico.id == servico_id
        )
    )

    if not servico:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Serviço não encontrado'
        )
    
    if servico.status == 'pendente':
        servico.status = 'concluido'
    else:
        servico.status='pendente'
        

    session.commit()
    session.refresh(servico)

    return servico



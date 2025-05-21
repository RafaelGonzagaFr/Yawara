

from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pytest import Session
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from yawara.database import get_session
from yawara.models import Funcionario, Pet, Usuario
from yawara.schemas import PetList, PetListComDono, PetResponse, PetSchema
from yawara.security import get_current_user

router = APIRouter(prefix='/pets', tags=['pets'])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[Usuario, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.OK, response_model=PetResponse)
def criar_novo_pet(pet: PetSchema, session: T_Session):
    db_user = session.scalar(
        select(Usuario).where(
            (Usuario.id == pet.dono)
        )
    )

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Esse cliente não existe'
        )

    db_funcionario = session.scalar(
       select(Funcionario).where(
          (Funcionario.id == db_user.id)
       )
    )

    if db_funcionario:
          raise HTTPException(
              status_code=HTTPStatus.BAD_REQUEST,
              detail='Esse usuário é um funcionário'
          )

    db_pet = Pet(
        nome=pet.nome,
        dono=pet.dono
    )

    session.add(db_pet)
    session.commit()
    session.refresh(db_pet)

    return db_pet


@router.get('/', status_code=HTTPStatus.OK, response_model=PetListComDono)
def listar_pets(session: T_Session):
    db_pets = session.scalars(
        select(Pet).join(Pet.cliente).options(selectinload(Pet.cliente))
    ).all()
    return {'pets': db_pets}

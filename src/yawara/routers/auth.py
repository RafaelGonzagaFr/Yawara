from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from yawara.database import get_session
from yawara.models import Usuario
from yawara.schemas import Token
from yawara.security import create_access_token, verify_password

router = APIRouter(prefix='/token', tags=['token'])
T_Session = Annotated[Session, Depends(get_session)]


@router.post('/', response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    """Rota de token"""
    usuario = session.scalar(
        select(Usuario).where(Usuario.login == form_data.username)
    )

    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )

    if not verify_password(form_data.password, usuario.senha):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect username or password',
        )

    access_token = create_access_token(data={'sub': usuario.username})

    return {'access_token': access_token, 'token_type': 'bearer'}
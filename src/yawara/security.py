from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from jwt import ExpiredSignatureError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from yawara.database import get_session
from yawara.models import Usuario
from yawara.settings import Settings


pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=Settings().ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, Settings().SECRET_KEY, algorithm=Settings().ALGORITHM)
    print(encoded_jwt)
    return encoded_jwt


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    print(session)
    print(token)
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(
            token, Settings().SECRET_KEY, algorithms=[Settings().ALGORITHM]
        )
        username: str = payload.get('sub')
        if not username:
            raise credentials_exception

    except ExpiredSignatureError:
        raise credentials_exception

    except PyJWTError:
        raise credentials_exception

    user = session.scalar(select(Usuario).where(Usuario.login == username))

    if not user:
        raise credentials_exception

    return user
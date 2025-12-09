import os
from fastapi import Header, HTTPException
import jwt

JWT_SECRET = os.getenv('JWT_SECRET')
JWT_ALG = os.getenv('JWT_ALGORITHM', 'HS256')


async def verify_jwt(authorization: str | None = Header(None)):
    if not authorization or not authorization.startswith('Bearer '):
        raise HTTPException(status_code=401, detail='Токен не правильный')
    token = authorization.split(' ', 1)[1]
    try:
        decode_jwt = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Ошибка с токеном')
    return decode_jwt

# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
#  Copyright 2020 yafra.org
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# -------------------------------------------------------------------------------
#
# YAPKI System User
from datetime import datetime
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette import status

from . import security
from settings import settings
from .database import get_db
from ..model.db import DbUser

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/login/access-token")



def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
):
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[security.ALGORITHM]
        )
        # token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    #user = crud.get_user(db, user_id=token_data.sub)
    #if not user:
    #    raise HTTPException(status_code=404, detail="User not found")
    #return user


def get_current_superuser(current_user: DbUser = Depends(get_current_user)):
    if not current_user.email == settings.super_user_email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not the superuser"
        )
    return current_user

def decode_time(obj, format):
    try:
        parsed_date = datetime.strptime(obj, format)
        return parsed_date.strftime("%Y-%m-%dT%H:%M:%S")
    except:
        return 0

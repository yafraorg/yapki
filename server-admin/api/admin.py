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
# YAPKI CLI
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from control import certificate
from utils.database import get_db
from model import schemas, db

apirouter = APIRouter()


@apirouter.get("/certificate/", response_model=List[schemas.Certificate])
def read_certificate(db: Session = Depends(get_db)):
    db_certificates = certificate.get_certificates(db)
    if db_certificates == 0:
        raise HTTPException(status_code=400, detail="no certificates in database")
    return db_certificates




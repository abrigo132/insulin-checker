from fastapi import APIRouter, Request, Depends
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from core import settings
from core.models import db_helper


router = APIRouter(prefix=settings.api.v1.insulin, tags=["insulin"])

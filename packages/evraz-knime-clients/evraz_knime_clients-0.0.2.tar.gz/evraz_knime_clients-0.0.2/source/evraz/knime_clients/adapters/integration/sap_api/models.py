from datetime import datetime

from pydantic import BaseModel, Field


class Header(BaseModel):
    version: str
    messageType: str
    messageText: str
    systemName: str
    uuId: str
    createDateTime: datetime
    currentPack: int
    totalPack: int
    statusCode: str
    statusComment: str


class ReportSap(BaseModel):
    header: Header
    metadata: dict | None = Field(default=None)
    data: list[dict]


class SchemeSap(BaseModel):
    header: Header
    metadata: dict


class HeaderSap(BaseModel):
    header: Header

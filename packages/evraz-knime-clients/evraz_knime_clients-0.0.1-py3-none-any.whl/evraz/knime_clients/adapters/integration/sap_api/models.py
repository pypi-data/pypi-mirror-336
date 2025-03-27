from pydantic import BaseModel, Field


class ReportSap(BaseModel):
    header: dict
    metadata: dict | None = Field(default=None)
    data: list[dict]


class SchemeSap(BaseModel):
    header: dict
    metadata: dict

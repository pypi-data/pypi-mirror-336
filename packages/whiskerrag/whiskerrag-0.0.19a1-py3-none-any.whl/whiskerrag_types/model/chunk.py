from datetime import datetime, timezone
from typing import Any, List, Optional, Union
from uuid import uuid4

from pydantic import (
    BaseModel,
    Field,
    field_serializer,
    field_validator,
    model_validator,
)

from whiskerrag_types.model.knowledge import EmbeddingModelEnum
from whiskerrag_types.model.utils import parse_datetime


class Chunk(BaseModel):
    chunk_id: str = Field(default_factory=lambda: str(uuid4()), description="chunk id")
    space_id: str = Field(..., description="space id")
    tenant_id: str = Field(..., description="tenant id")
    embedding: Optional[list[float]] = Field(None, description="chunk embedding")
    context: str = Field(..., description="chunk content")
    knowledge_id: str = Field(..., description="file source info")
    embedding_model_name: Optional[EmbeddingModelEnum] = Field(
        EmbeddingModelEnum.OPENAI, description="name of the embedding model"
    )
    metadata: Optional[dict] = Field(
        None, description="Arbitrary metadata associated with the content."
    )
    created_at: Optional[datetime] = Field(
        default=None,
        alias="gmt_create",
        description="creation time",
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        alias="gmt_modified",
        description="update time",
    )

    @field_validator("embedding", mode="before")
    @classmethod
    def parse_embedding(cls, v: Union[str, List[float], None]) -> Optional[List[float]]:
        if v is None:
            return None

        if isinstance(v, list):
            return [float(x) for x in v]

        if isinstance(v, str):
            v = v.strip()
            try:
                import json

                return (
                    [float(x) for x in json.loads(v)]
                    if isinstance(json.loads(v), list)
                    else None
                )
            except json.JSONDecodeError:
                try:
                    if v.startswith("[") and v.endswith("]"):
                        v = v[1:-1]
                    return [float(x.strip()) for x in v.split(",") if x.strip()]
                except ValueError:
                    raise ValueError(f"Invalid embedding format: {v}")

        raise ValueError(f"Unsupported embedding type: {type(v)}")

    @field_serializer("embedding_model_name")
    def serialize_embedding_model_name(
        self, embedding_model_name: Optional[EmbeddingModelEnum]
    ) -> Optional[str]:
        return embedding_model_name.value if embedding_model_name else None

    def update(self, **kwargs: Any) -> "Chunk":
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.updated_at = datetime.now(timezone.utc)
        return self

    @model_validator(mode="before")
    def ensure_aware_timezones(cls, values: dict) -> dict:
        field_mappings = {"created_at": "gmt_create", "updated_at": "gmt_modified"}
        for field, alias_name in field_mappings.items():
            val = values.get(field) or values.get(alias_name)
            if val is None:
                continue

            if isinstance(val, str):
                dt = parse_datetime(val)
                values[field] = dt
                values[alias_name] = dt
            else:
                if val and val.tzinfo is None:
                    dt = val.replace(tzinfo=timezone.utc)
                    values[field] = dt
                    values[alias_name] = dt

        return values

    @model_validator(mode="after")
    def set_defaults(self) -> "Chunk":
        now = datetime.now(timezone.utc)
        if self.created_at is None:
            self.created_at = now
        if self.updated_at is None:
            self.updated_at = now
        return self

    class Config:
        allow_population_by_field_name = True

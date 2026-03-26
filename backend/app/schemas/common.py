from datetime import datetime

from pydantic import BaseModel, Field


class MongoModel(BaseModel):
    id: str = Field(alias="_id")
    created_at: datetime
    updated_at: datetime

    model_config = {"populate_by_name": True}

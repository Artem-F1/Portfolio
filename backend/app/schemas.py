from pydantic import BaseModel, Field, ConfigDict
import uuid


class TaskSchema(BaseModel):
    id: uuid.UUID
    title: str = Field(min_length=1)
    completed: bool = Field(..., validation_alias="is_completed", serealization_alias="completed")
    

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

        
class TaskCreate(BaseModel):
    title: str

        
class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    completed: bool | None = Field(default=None, alias="is_completed")
    model_config = ConfigDict(populate_by_name=True)
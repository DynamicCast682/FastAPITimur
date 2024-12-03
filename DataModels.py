from enum import Enum

from pydantic import field_validator
from pydantic import BaseModel



class Status(BaseModel):
  status: str

  @staticmethod
  @field_validator("status")
  def validate_status(status: str) -> str:
    if status != "ok" and status != "error":
      raise ValueError("Status must be 'ok' or 'error'")
    return status

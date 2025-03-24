from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime

class Chat(BaseModel):

    class Config:
        orm_mode = True
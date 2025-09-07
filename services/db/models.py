from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, conlist
from bson.objectid import ObjectId

# --- Pydantic Models for MongoDB Schema ---
# These models help enforce a consistent structure when you create new documents.

class PyObjectId(ObjectId):
    """
    A custom type for Pydantic to handle MongoDB's ObjectId.
    """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        json_schema = handler(core_schema)
        json_schema.update(type="string")
        return json_schema

class User(BaseModel):
    """
    Represents a user document in the 'users' collection.
    """
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: str
    displayName: str
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class File(BaseModel):
    """
    Represents a file document in the 'files' collection.
    """
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    userId: PyObjectId
    originalFileName: str
    s3Key: str
    fileSize: int
    uploadDate: datetime = Field(default_factory=datetime.utcnow)
    extractedDataId: Optional[PyObjectId]
    rawText: Optional[str]
    embeddings: Optional[List[conlist(float, min_length=1)]] 

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class ExtractedData(BaseModel):
    """
    Represents a document in the 'extracted_data' collection.
    The 'extractedFields' field can have a flexible structure.
    """
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    fileId: PyObjectId
    dataType: str
    extractedFields: Dict[str, Any]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

from typing import Dict, Any, List, Optional
from bson.objectid import ObjectId
from datetime import datetime
from services.db.models import File as FileMode, ExtractedData, PyObjectId

def insert_extracted_data(db, file_id: str, data_type: str, extracted_fields: Dict[str, Any]) -> ObjectId:
    """
    Inserts a new extracted data document and returns its ObjectId.
    """
    extracted_doc = ExtractedData(
        fileId=PyObjectId(file_id),
        dataType=data_type,
        extractedFields=extracted_fields
    )
    result = db["extracted_data"].insert_one(extracted_doc.dict(by_alias=True))
    return result.inserted_id

def update_file_metadata(db, file_id: str, raw_text: str, embeddings: List[List[float]], extracted_data_id: ObjectId):
    """
    Updates the file document with raw text, embeddings, and extractedDataId.
    """
    db["files"].update_one(
        {"_id": ObjectId(file_id)},
        {"$set": {
            "rawText": raw_text,
            "embeddings": embeddings,
            "extractedDataId": extracted_data_id
        }}
    )


def insert_file_metadata(db, file_doc: dict):
    validated_file_doc = FileModel(**file_doc)
    result = db["files"].insert_one(validated_file_doc.dict(by_alias=True))
    return result.inserted_id
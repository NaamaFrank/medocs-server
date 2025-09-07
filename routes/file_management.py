import os
import boto3
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, BackgroundTasks
from pydantic import ValidationError
from datetime import datetime
from bson.objectid import ObjectId
from services.db.client import get_mongo_client
from services.db.models import File as FileModel, PyObjectId
from utils.config import AWS_ACCESS_KEY,AWS_SECRET_ACCESS_KEY, S3_BUCKET_NAME
from services.ai_pipeline import run_ai_pipeline
from services.db.dao.file_dao import insert_file_metadata

router = APIRouter()

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

@router.post("/api/upload")
async def upload_file(file: UploadFile = File(...), background_tasks: BackgroundTasks):
    """
    Handles the file upload process, uploads to S3, and saves metadata to MongoDB.
    """
    if not S3_BUCKET_NAME:
        raise HTTPException(status_code=500, detail="S3_BUCKET_NAME not configured.")
    
    # Placeholder for the user's ID. In a real application, you would
    # get this from the authenticated user's session or token.
    user_id = "123456789012345678901234" # Example placeholder ID
    
    # Generate a unique key for S3 to avoid filename collisions
    s3_key = f"uploads/{user_id}/{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"

    try:
        # Step 1: Upload file to S3
        file_content = await file.read()

        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=s3_key,
            Body=file_content,
            ContentType=file.content_type
        )

        # Step 2: Get a database connection
        client = get_mongo_client()
        if not client:
            raise HTTPException(status_code=500, detail="Failed to connect to the database.")
        
        db = client["medocs"]

        # Step 3: Prepare the document for MongoDB
        file_doc = {
            "userId": PyObjectId(user_id),
            "originalFileName": file.filename,
            "s3Key": s3_key,
            "fileSize": len(file_content),
            "uploadDate": datetime.utcnow(),
            "extractedDataId": None, # Will be added later
            "rawText": "", # Will be populated by the AI pipeline
            "embeddings": [] # Will be populated by the AI pipeline
        }

        # Save the file metadata to MongoDB
        file_id = str(insert_file_metadata(db, file_doc))
        # Run the AI pipeline in the background
        background_tasks.add_task(run_ai_pipeline, file_content, s3_key, file_id)
        return {"message": "File uploaded and metadata saved successfully", "file_id": file_id}

    except ValidationError as e:
        # Handle schema validation errors
        raise HTTPException(status_code=400, detail=f"Data validation failed: {e}")
    except Exception as e:
        # General error handling for S3 or MongoDB issues
        raise HTTPException(status_code=500, detail=str(e))

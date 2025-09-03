import os
import uuid
import boto3
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from ..utils.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET_NAME

# Create an APIRouter instance
api_router = APIRouter(prefix="/api")

@api_router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Handles a file upload request from the frontend.
    It receives a file, uploads it to an S3 bucket, and returns the file's URL.
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file part in the request")

    if file.filename == '':
        raise HTTPException(status_code=400, detail="No selected file")

    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

        original_filename = file.filename
        file_extension = os.path.splitext(original_filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"

        # Upload the file object directly to S3
        s3_client.upload_fileobj(
            file.file,
            S3_BUCKET_NAME,
            unique_filename
        )

        file_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{unique_filename}"

        return JSONResponse(content={
            'message': 'File uploaded successfully!',
            'url': file_url
        }, status_code=200)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during the upload process: {str(e)}"
        )

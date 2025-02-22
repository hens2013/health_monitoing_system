from fastapi import APIRouter, Query, HTTPException, Depends
from fastapi.responses import FileResponse
import os

from db.database import get_db
from app.utils.health_score import generate_pdf_report  # Import your function
from app.logger import logging
from sqlalchemy.ext.asyncio import AsyncSession

users_router = APIRouter()


@users_router.get("/get_health_score", response_class=FileResponse)
async def get_health_score(user_id: int = Query(..., description="User ID to generate health score report"),
                           db: AsyncSession = Depends(get_db)):
    """
    API Endpoint to generate and return a health score report for a user.
    """
    pdf_file_path = f"health_report_user_{user_id}.pdf"

    try:
        logging.info(f"Generating health report for user {user_id}...")
        await generate_pdf_report(user_id)
    except Exception as e:
        logging.error(f"Error generating health report: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate health report.")

    if not os.path.exists(pdf_file_path):
        logging.error("Report file not found after generation.")
        raise HTTPException(status_code=500, detail="Report generation failed.")

    return FileResponse(pdf_file_path, filename=f"health_report_{user_id}.pdf", media_type="application/pdf")

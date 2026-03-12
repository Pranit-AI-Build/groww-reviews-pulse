"""Reports API endpoints."""

import json
from typing import List, Dict, Any, Optional
from pathlib import Path
from fastapi import APIRouter, HTTPException

from app.core.config import get_settings

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("/latest")
async def get_latest_report():
    """Get the latest weekly pulse report."""
    settings = get_settings()
    
    report_path = settings.latest_report_path
    
    if not report_path.exists():
        raise HTTPException(status_code=404, detail="No reports found")
    
    with open(report_path, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    return report


@router.get("/list")
async def list_reports() -> List[Dict[str, str]]:
    """List all available reports."""
    settings = get_settings()
    
    reports = []
    if settings.latest_report_path.exists():
        reports.append({
            "id": "latest",
            "name": "Latest Weekly Pulse",
            "path": str(settings.latest_report_path)
        })
    
    return reports


@router.get("/{report_id}")
async def get_report(report_id: str):
    """Get a specific report by ID."""
    settings = get_settings()
    
    if report_id == "latest":
        report_path = settings.latest_report_path
    else:
        report_path = settings.reports_dir / f"{report_id}.json"
    
    if not report_path.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    
    with open(report_path, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    return report

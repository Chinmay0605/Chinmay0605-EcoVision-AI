from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException
)

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from pathlib import Path

import shutil
import uuid


# =========================================================
# AGENTS
# =========================================================

from backend.agents.vision_agent import (
    vision_agent
)

from backend.agents.classification_agent import (
    classification_agent
)

from backend.agents.knowledge_agent import (
    knowledge_agent
)

from backend.agents.recommendation_agent import (
    recommendation_agent
)

from backend.agents.disposal_agent import (
    disposal_agent
)

from backend.agents.report_agent import (
    report_agent
)


# =========================================================
# DATABASE
# =========================================================

from backend.database.database import (
    init_database,
    save_scan,
    get_scan_history,
    get_statistics,
    delete_all_scans,
    delete_scan
)


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="EcoVision AI",
    description=(
        "AI-powered household waste analysis "
        "and local disposal intelligence system"
    ),
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# DIRECTORIES
# =========================================================

BASE_DIR = Path(
    __file__
).resolve().parent.parent


UPLOAD_DIR = (
    BASE_DIR /
    "data" /
    "uploads"
)


REPORT_DIR = (
    BASE_DIR /
    "reports"
)


UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


REPORT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# STATIC FILES
# =========================================================

app.mount(
    "/uploads",
    StaticFiles(
        directory=str(UPLOAD_DIR)
    ),
    name="uploads"
)


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

init_database()


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "message": "Welcome to EcoVision AI",
        "status": "running"
    }


# =========================================================
# ANALYZE WASTE IMAGE
# =========================================================

@app.post("/api/analyze")
async def analyze_waste(
    file: UploadFile = File(...)
):

    # -----------------------------------------------------
    # Validate file type
    # -----------------------------------------------------

    allowed_types = [
        "image/jpeg",
        "image/png",
        "image/jpg",
        "image/webp"
    ]

    if file.content_type not in allowed_types:

        return {
            "status": "error",
            "message": "Please upload a valid image.",
            "allowed_types": allowed_types
        }


    # -----------------------------------------------------
    # Generate unique filename
    # -----------------------------------------------------

    file_extension = Path(
        file.filename or ""
    ).suffix.lower()


    unique_filename = (
        f"{uuid.uuid4()}{file_extension}"
    )


    file_path = (
        UPLOAD_DIR /
        unique_filename
    )


    # -----------------------------------------------------
    # Save uploaded image
    # -----------------------------------------------------

    try:

        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

    except Exception as e:

        return {
            "status": "error",
            "message":
                "Failed to save uploaded image.",
            "error": str(e)
        }


    # -----------------------------------------------------
    # Vision Agent
    # -----------------------------------------------------

    try:

        analysis = vision_agent.analyze(
            str(file_path)
        )

    except Exception as e:

        return {
            "status": "error",
            "message":
                "AI vision analysis failed.",
            "error": str(e)
        }


    # -----------------------------------------------------
    # Confidence Intelligence
    # -----------------------------------------------------

    confidence = analysis["confidence"]


    if confidence >= 70:

        confidence_level = "High"

        confidence_status = "trusted"

        confidence_message = (
            "The AI is highly confident "
            "in this prediction."
        )


    elif confidence >= 45:

        confidence_level = "Medium"

        confidence_status = "review"

        confidence_message = (
            "The AI has moderate confidence. "
            "Review the alternative predictions "
            "before disposal."
        )


    else:

        confidence_level = "Low"

        confidence_status = "uncertain"

        confidence_message = (
            "The AI has low confidence. "
            "Please verify the item manually."
        )


    # -----------------------------------------------------
    # Classification Agent
    # -----------------------------------------------------

    try:

        classification = (
            classification_agent.classify(
                analysis
            )
        )

    except Exception as e:

        return {
            "status": "error",
            "message":
                "Waste classification failed.",
            "error": str(e)
        }


    # -----------------------------------------------------
    # Knowledge Agent
    # -----------------------------------------------------

    try:

        knowledge = (
            knowledge_agent.get_knowledge(
                classification["category"]
            )
        )

    except Exception as e:

        return {
            "status": "error",
            "message":
                "Waste knowledge lookup failed.",
            "error": str(e)
        }


    # -----------------------------------------------------
    # Recommendation Agent
    # -----------------------------------------------------

    try:

        recommendation = (
            recommendation_agent.generate(
                classification,
                knowledge
            )
        )

    except Exception as e:

        return {
            "status": "error",
            "message":
                "Recommendation generation failed.",
            "error": str(e)
        }


    # -----------------------------------------------------
    # Save Scan To Database
    # -----------------------------------------------------

    try:

        scan_id = save_scan(

            filename=file.filename,

            stored_filename=unique_filename,

            waste_type=analysis["label"],

            category=classification["category"],

            material=classification["material"],

            confidence=analysis["confidence"],

            recyclable=classification["recyclable"],

            recommended_bin=(
                recommendation[
                    "recommended_bin"
                ]
            ),

            disposal_instruction=(
                recommendation[
                    "disposal_instruction"
                ]
            ),

            handling_instruction=(
                recommendation[
                    "handling_instruction"
                ]
            ),

            eco_tip=(
                recommendation[
                    "eco_tip"
                ]
            )
        )

    except Exception as e:

        return {
            "status": "error",
            "message":
                "Analysis succeeded but scan "
                "could not be saved.",
            "error": str(e)
        }


    # -----------------------------------------------------
    # Final Response
    # -----------------------------------------------------

    return {

        "status": "success",

        "scan_id": scan_id,

        "filename": file.filename,

        "image_url": (
            f"/uploads/{unique_filename}"
        ),

        "analysis": {

            "waste_type":
                analysis["label"],

            "confidence":
                analysis["confidence"],

            "confidence_level":
                confidence_level,

            "confidence_status":
                confidence_status,

            "confidence_message":
                confidence_message,

            "alternatives":
                analysis["alternatives"],

            "classification":
                classification,

            "knowledge":
                knowledge,

            "recommendation":
                recommendation
        }
    }


# =========================================================
# GET SCAN HISTORY
# =========================================================

@app.get("/api/history")
def history():

    scans = get_scan_history()


    return {

        "status": "success",

        "count": len(scans),

        "scans": scans
    }


# =========================================================
# DELETE ONE SCAN
# =========================================================

@app.delete("/api/history/{scan_id}")
def delete_single_scan(
    scan_id: int
):

    deleted = delete_scan(
        scan_id
    )


    if not deleted:

        return {

            "status": "error",

            "message": "Scan not found."

        }


    return {

        "status": "success",

        "message":
            "Scan deleted successfully.",

        "scan_id":
            scan_id
    }


# =========================================================
# DELETE ALL SCANS
# =========================================================

@app.delete("/api/history")
def clear_history():

    delete_all_scans()


    return {

        "status": "success",

        "message":
            "All scan history has been deleted."
    }


# =========================================================
# DASHBOARD STATISTICS
# =========================================================

@app.get("/api/stats")
def statistics():

    stats = get_statistics()


    return {

        "status": "success",

        "stats": stats
    }


# =========================================================
# LOCAL DISPOSAL INTELLIGENCE
# =========================================================

@app.get("/api/local-disposal")
def local_disposal(

    category: str = "General Waste",

    city: str = "Indore"

):

    try:

        guidance = (
            disposal_agent.get_guidance(
                category=category,
                city=city
            )
        )


        return {

            "status": "success",

            "guidance": guidance

        }


    except Exception as e:

        return {

            "status": "error",

            "message":
                "Failed to get local disposal guidance.",

            "error": str(e)

        }


# =========================================================
# GENERATE PDF REPORT
# =========================================================

@app.get("/api/report/{scan_id}")
def generate_scan_report(

    scan_id: int,

    city: str = "Indore"

):

    # -----------------------------------------------------
    # Find scan
    # -----------------------------------------------------

    scans = get_scan_history(
        limit=1000
    )


    scan = next(
        (
            item
            for item in scans
            if item["id"] == scan_id
        ),
        None
    )


    if scan is None:

        raise HTTPException(
            status_code=404,
            detail="Scan not found."
        )


    # -----------------------------------------------------
    # Get local disposal guidance
    # -----------------------------------------------------

    try:

        local_guidance = (
            disposal_agent.get_guidance(

                category=scan.get(
                    "category",
                    "General Waste"
                ),

                city=city

            )
        )

    except Exception:

        # Fallback so report generation
        # never fails because of guidance.

        local_guidance = {

            "city": city,

            "category":
                scan.get(
                    "category",
                    "General Waste"
                ),

            "local_instruction":
                (
                    "Follow local municipal "
                    "waste-segregation rules "
                    "and use the appropriate "
                    "waste stream."
                ),

            "important_note":
                (
                    "Local collection rules and "
                    "authorized facilities can change. "
                    "Verify current municipal guidance "
                    "before disposal."
                )
        }


    # -----------------------------------------------------
    # Find uploaded image
    # -----------------------------------------------------

    stored_filename = scan.get(
        "stored_filename"
    )


    if not stored_filename:

        raise HTTPException(
            status_code=404,
            detail="Original uploaded image not found."
        )


    image_path = (
        UPLOAD_DIR /
        stored_filename
    )


    if not image_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Original uploaded image file not found."
        )


    # -----------------------------------------------------
    # Report file path
    # -----------------------------------------------------

    report_path = (
        REPORT_DIR /
        f"EcoVision_Report_{scan_id}.pdf"
    )


    # -----------------------------------------------------
    # Generate report using ReportAgent
    # -----------------------------------------------------

    try:

        generated_report = (
            report_agent.generate_report(

                scan=scan,

                image_path=str(
                    image_path
                ),

                output_path=str(
                    report_path
                ),

                local_guidance=local_guidance

            )
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                "PDF report generation failed: "
                f"{str(e)}"
            )
        )


    # -----------------------------------------------------
    # Return PDF
    # -----------------------------------------------------

    return FileResponse(

        path=str(
            generated_report
        ),

        media_type="application/pdf",

        filename=(
            f"EcoVision_Report_{scan_id}.pdf"
        ),

        headers={
            "Content-Disposition":
                (
                    "inline; "
                    f'filename="EcoVision_Report_{scan_id}.pdf"'
                )
        }

    )
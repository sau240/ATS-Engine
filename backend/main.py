from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import traceback

# Rate limiting imports
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# importing logic of the code.
import ats_engine 

# --- CONFIGURATION ---
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="ATS Resume Checker API")
app.state.limiter = limiter

# FIX 1: Removed the stray 'p' at the end of the line
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ENDPOINTS ---

@app.post("/scan")
@limiter.limit("6/minute") 
async def scan_resume(
    request: Request, 
    resume_file: UploadFile = File(...), 
    jd_text: str = Form(...)
):
    try: 
        # File type validation
        if not resume_file.filename.lower().endswith(('.pdf', '.docx')):
            raise HTTPException(status_code=400, detail="Only PDF or Word (.docx) files are allowed.")

        # Read the file into memory
        file_bytes = await resume_file.read() 
        
        # FIX 2: Added more robust error checking for the extraction process
        resume_text = ats_engine.extract_text_from_pdf_stream(file_bytes)
        
        # If the text is empty, we shouldn't attempt the scan as it will crash the math logic
        if not resume_text.strip():
            return {
                "status": "error",
                "message": "Could not extract text from the PDF. It might be scanned as an image."
            }

        # Process using your engine
        results = ats_engine.ats_scan(resume_text, jd_text)
        
        # Cleanup
        await resume_file.close()
        
        return {
            "status": "success",
            "data": results
        }
        
    except Exception as e:
        # This will print the exact line number of the crash in your terminal
        print("--- BACKEND ERROR LOG ---")
        print(traceback.format_exc()) 
        print("-------------------------")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/")
def home():
    return {"message": "ATS Backend is running!"}

if __name__ == "__main__":
    # Ensure port matches what React is calling (8000)
    uvicorn.run(app, host="127.0.0.1", port=8000)
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import ValidationError
import json
from models import Product

app = FastAPI(title="Strict Validator API")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

@app.post("/api/validate")
async def validate_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.json'):
        raise HTTPException(status_code=400, detail="Only JSON files are allowed.")
    
    try:
        content = await file.read()
        data = json.loads(content)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not read file: {str(e)}")
        
    if not isinstance(data, list):
        raise HTTPException(status_code=400, detail="JSON data should be a list of products.")
        
    valid_products = []
    errors = []
    
    for idx, item in enumerate(data):
        try:
            product = Product(**item)
            valid_products.append(product.model_dump())
        except ValidationError as e:
            clean_errors = [{"loc": err.get("loc", []), "msg": err.get("msg", "")} for err in e.errors()]
            errors.append({"index": idx, "item": item, "errors": clean_errors})
            
    summary = {
        "total": len(data),
        "valid_count": len(valid_products),
        "invalid_count": len(errors),
        "errors": errors
    }
    
    return JSONResponse(content=summary)

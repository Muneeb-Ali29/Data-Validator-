# Data Validator - FastAPI & CLI

This project is a strict configuration and data validation tool built with Python. It features both a Command-Line Interface (CLI) and a web API built with FastAPI. It leverages Pydantic for robust data validation and environment variable management.

## Features

- **Pydantic Data Validation**: Ensures that product data adheres strictly to defined schemas (e.g., non-empty names, positive prices).
- **Environment Configuration**: Securely loads environment variables (like API keys) using `pydantic-settings` from a `.env` file.
- **FastAPI Web Interface**: Exposes an endpoint (`/api/validate`) to upload and validate JSON files containing product data. It also serves a static HTML frontend.
- **CLI Tool**: A standalone command-line script (`main.py`) to validate local JSON files directly from your terminal.

## Usage

### 1. Using the Command-Line Interface (CLI)
You can validate a JSON file directly via the CLI:
```bash
python main.py data.json
```
This will output a summary of valid and invalid products, along with specific error messages for any validation failures.

### 2. Using the FastAPI Web Application
Start the FastAPI server using Uvicorn:
```bash
uvicorn app:app --reload
```
- Open your browser and navigate to `http://localhost:8000` to access the frontend interface.
- You can upload a JSON file through the UI to get a validation summary.
- API documentation is automatically generated and accessible at `http://localhost:8000/docs`.

## Project Structure

- `app.py`: The FastAPI application and endpoints.
- `main.py`: The CLI application for local file validation.
- `models.py`: Pydantic models for product schema and configuration settings.
- `data.json`: A sample data file for testing.
- `static/`: Contains the frontend static files (HTML, CSS, JS).
- `requirements.txt`: Python dependencies.
- `.env`: Environment variables (do not commit this file to GitHub).

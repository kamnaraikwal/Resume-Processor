## Features and what it does

- Upload PDF resumes through a REST API
- Store file metadata and status in MongoDB
- Process uploads asynchronously through an RQ queue
- Convert PDF pages into JPEG images with Poppler
- Analyze resumes with Google Gemini
- Retrieve processing status and results by file ID
- Run the API, worker, and Valkey queue with Docker Compose

## Architecture

- **FastAPI**: Upload and status HTTP endpoints
- **RQ**: Asynchronous background job queue
- **Valkey/Redis**: RQ message broker
- **MongoDB**: File metadata and generated results
- **pdf2image + Poppler**: PDF-to-image conversion
- **Google Gemini**: Resume analysis and text generation

### Start the services

```powershell
docker compose up --build
```

This starts:

- API server on `http://localhost:8000`
- RQ worker
- Valkey on port `6379`

### Stop the services

```powershell
docker compose down -v
```

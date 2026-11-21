Write-Host "Starting GlobeWise backend and frontend..."

Start-Process powershell -ArgumentList '-NoExit', '-Command', "cd '$PSScriptRoot\backend'; .\.venv\Scripts\python.exe -m uvicorn app.main:app --reload"

Start-Process powershell -ArgumentList '-NoExit', '-Command', "cd '$PSScriptRoot\frontend'; npm run dev"

Write-Host "Backend:  http://127.0.0.1:8000  (API docs: http://127.0.0.1:8000/docs)"
Write-Host "Frontend: http://localhost:5173"

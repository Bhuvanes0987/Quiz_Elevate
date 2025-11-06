
QuizElevate - Project (Linked to your existing MySQL DB)
========================================================

This package contains a Flask backend and a minimal frontend scaffold.
It is preconfigured to connect to your existing MySQL database named `quizelevate`.

1) Link backend to your MySQL database:
   - Copy backend/.env.example to backend/.env and set MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD appropriately.
   - Make sure the database 'quizelevate' exists and is accessible from the machine running the backend.

2) Install and run backend locally:
   - cd backend
   - python -m venv .venv && source .venv/bin/activate
   - pip install -r requirements.txt
   - export FLASK_APP=app.main:create_app
   - flask db init
   - flask db migrate -m "initial"
   - flask db upgrade
   - python -m app.main

3) Open frontend demo:
   - open frontend/src/index.html in a browser to test OTP flow (calls localhost:8000).

Notes:
- OTPs are printed to the backend console for development. Replace app/utils/otp_service.py to integrate SMS/email.
- AI evaluation is a local stub in app/utils/ai_eval.py. When you host Ollama, replace stub with HTTP calls to Ollama endpoint.
- The provided docker-compose is only for running the backend container and assumes your MySQL server is external (already set up).



venv\Scripts\activate
cd backend
python -m app.main       

ng serve
ng generate component pages/login-page
cd frontend
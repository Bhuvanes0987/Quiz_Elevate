
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
ENV FLASK_APP=app.main:create_app
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app.main:create_app()"]

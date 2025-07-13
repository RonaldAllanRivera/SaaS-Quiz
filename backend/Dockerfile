# Backend Dockerfile for PRODUCTION/DEPLOY (Railway, etc)
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8000

# Use CMD for prod (can be overridden by Railway/etc)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

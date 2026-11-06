FROM python:3.11-slim
WORKDIR /app

COPY *.py ./
CMD ["python", "oop_auditor.py"]

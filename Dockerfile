FROM python:3.11-slim
WORKDIR /app

COPY *.py ./
CMD ["python", "week8lab_oop_auditor.py"]

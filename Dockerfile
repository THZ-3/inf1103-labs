FROM python:3.11-slim
WORKDIR /app

COPY product.py inventory.py file_handler.py week8lab_oop_auditor.py ./
CMD ["python", "week8lab_oop_auditor.py"]

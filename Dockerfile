FROM python:3.11-slim
WORKDIR /app

#lab-2
#COPY auditor.py . 
#CMD ["python", "auditor.py"] 

#lab3
COPY modular_auditor.py . 
CMD ["python", "modular_auditor.py"] 

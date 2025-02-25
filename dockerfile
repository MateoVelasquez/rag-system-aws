FROM python:3.13-slim

WORKDIR /rag_system

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

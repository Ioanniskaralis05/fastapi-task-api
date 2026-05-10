FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install fastapi uvicorn

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
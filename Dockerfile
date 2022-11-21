FROM python:latest
WORKDIR /app
COPY . .
RUN pip3 install poetry
RUN poetry config virtualenvs.create false && poetry install
EXPOSE 8000
CMD ["uvicorn","app.main:app","--host=0.0.0.0","--reload"]


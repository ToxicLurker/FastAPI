FROM python:3.8.2

RUN mkdir app

COPY . /app

RUN cd app \
    && pip install poetry \
    && poetry install

RUN ls

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "src.test_project.funcs:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# CMD ["sleep", "1000"]

WORKDIR /app
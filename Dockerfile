FROM python:3.9

ARG USERNAME=developer

ENV POETRY_HOME=/home/$USERNAME
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /app

COPY ./pyproject.toml ./

RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.1.15
RUN poetry install



COPY ./app /app

#CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
FROM python:3.10.11-slim

WORKDIR /code

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=off
ENV POETRY_VIRTUALENVS_CREATE=false

RUN pip install poetry

COPY pyproject.toml poetry.lock faiss_document_store.db /code/
COPY ./apis /code/apis
COPY ./model /code/model

RUN poetry install

RUN apt autoremove -y \
 && apt clean \
 && rm -rf /var/lib/apt/lists/* \
           /var/tmp/* \
           /usr/share/doc \
           /usr/share/man \
 # remove python files
 && rm -rf /root/.cache/pip/ \
 && find / -name '*.pyc' -delete \
 && find / -name '*__pycache__*' -delete \
 && find / -name '*.whl' -delete

CMD ["poetry", "run", "uvicorn", "apis.main:app", "--host", "0.0.0.0", "--port", "8000"]
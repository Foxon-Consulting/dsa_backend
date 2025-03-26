FROM python:3.12

# x-release-please-start-version
ARG PREFIX="document_sorting_assistant-0.0.0"
# x-release-please-end

WORKDIR /app
COPY . .
# COPY ./dist/$PREFIX-py3-none-any.whl ./$PREFIX-py3-none-any.whl
# RUN pip install --no-cache-dir --upgrade $PREFIX-py3-none-any.whl

RUN pip install --no-cache-dir --upgrade .
RUN pip install --no-cache-dir python-multipart

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]

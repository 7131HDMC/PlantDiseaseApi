FROM python:3.11

WORKDIR /plantDiseaseApi

COPY ./requirements.txt /plantDiseaseApi/requirements.txt

RUN pip install --no-cache-dir -r /plantDiseaseApi/requirements.txt

COPY ./app /plantDiseaseApi/app

EXPOSE 8000

CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]
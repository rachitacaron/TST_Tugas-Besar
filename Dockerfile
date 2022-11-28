FROM python:3.9
WORKDIR /tst_tugas-besar
COPY requirements.txt /tst_tugas-besar/requirements.txt
RUN pip install -r requirements.txt
COPY . /tst_tugas-besar
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
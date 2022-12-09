FROM python:3.9
EXPOSE 8080
WORKDIR /book_recommender_tst
COPY requirements.txt /book_recommender_tst/requirements.txt
RUN pip install -r requirements.txt
COPY . /book_recommender_tst
EXPOSE 8080
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
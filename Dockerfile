FROM python:3.9

COPY app /app
WORKDIR /app
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD [ "python", "flask_test.py" ]
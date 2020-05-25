FROM python:3.8.3

ADD code /code
RUN pip install -r /code/pip-requirements.txt

WORKDIR /code
ENV PYTHONPATH '/code/'
ENV FLASK_APP '/code/tangogql-proxy.py'

CMD ["flask" , "run", "--host=0.0.0.0"]
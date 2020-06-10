FROM tangocs/tango-pytango

USER root

RUN apt-get update && apt-get install curl -y

USER tango

ADD code /code
RUN pip install -r /code/pip-requirements.txt

WORKDIR /code
ENV PYTHONPATH '/code/'

CMD ["python" , "/code/collector.py"]
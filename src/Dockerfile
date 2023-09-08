FROM python:3.10-alpine

# Create stdconfig directory
WORKDIR /

COPY requirements.txt /
RUN pip install -r requirements.txt
COPY zenapi /zenapi
COPY static /static
COPY templates /templates
COPY solarflow-status.py /


ENTRYPOINT ["python","solarflow-status.py"]

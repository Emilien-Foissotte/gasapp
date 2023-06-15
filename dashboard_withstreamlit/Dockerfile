FROM python:3.9

# RUN apt-get update && apt-get upgrade -y

# RUN pip --upgrade pip
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

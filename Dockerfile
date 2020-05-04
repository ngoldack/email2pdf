FROM ubuntu

MAINTAINER Nicolas Goldack <nicolas-goldack@live.de>

WORKDIR /email2pdf/

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.8 \
    wkhtmltopdf \
    wget \
    python3-pip

RUN wget "https://chilkatdownload.com/9.5.0.82/chilkat-9.5.0-python-3.8-x86_64-linux.tar.gz" --no-check-certificate
RUN tar -zxvf "chilkat-9.5.0-python-3.8-x86_64-linux.tar.gz"
RUN cd chilkat-9.5.0-python-3.8-x86_64-linux && python3 installChilkat.py

ADD . .

RUN pip3 install -r requirements.txt


CMD ["python3", "-u", "email2pdf.py"]

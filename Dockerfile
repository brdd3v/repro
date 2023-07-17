FROM ubuntu:18.04

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        mysql-server \
        nano \
        python3 \
        python3-dev \
        python3-pip \
        python3-setuptools \
        unzip

WORKDIR /repro

RUN export PERL_MM_USE_DEFAULT=1 && \
        cpan ESTRABD/MySQL-Diff-0.60.tar.gz

COPY requirements.txt .

RUN pip3 --no-cache-dir install -r requirements.txt

COPY . .

RUN cp .my.cnf $HOME

CMD ["bash"]

FROM python:3.6
WORKDIR /app

COPY wands ./wands
COPY ./gunicorn.conf.py .
COPY ./requirements.txt .

ENV LANG C.UTF-8

RUN  apt-get update -y \
    && pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip3 install  gunicorn -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && apt-get install tzdata -y

CMD ["gunicorn", "wands.server.manage:app", "-c", "./gunicorn.conf.py","--access-logfile","-"]
FROM python:3.10-buster
ENV BOT_NAME=$BOT_NAME

WORKDIR /usr/src/app/"${BOT_NAME:-tg_bot}"

COPY requirements.txt /usr/src/app/"${BOT_NAME:-tg_bot}"
#RUN pip install pip install pydevd-pycharm~=223.8617.48
RUN pip install -r /usr/src/app/"${BOT_NAME:-tg_bot}"/requirements.txt
#COPY bot_app /usr/src/app/"${BOT_NAME:-tg_bot}"

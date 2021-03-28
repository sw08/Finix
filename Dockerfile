FROM python:3.8.6
WORKDIR /
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py
RUN git clone https://github.com/sw08/ThinkingBot-v2.git
WORKDIR /ThinkingBot-v2
RUN python -m pip install -r requirements.txt
COPY . /ThinkingBot-v2
CMD python bot.py
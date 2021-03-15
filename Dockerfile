FROM python:3.8.6
WORKDIR /
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py
RUN git clone https://github.com/sw08/Finix.git
WORKDIR /Finix
RUN python -m pip install -r requirements.txt
COPY . /Finix
CMD python bot.py
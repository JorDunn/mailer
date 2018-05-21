FROM ubuntu:latest

RUN git clone https://github.com/JorDunn/mailer.git mailer

WORKDIR mailer

EXPOSE 10100

ENTRYPOINT [ "run ]
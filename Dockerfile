FROM python:3

WORKDIR /app

COPY . /app

ENTRYPOINT [ "python", "src/main.py" ]

CMD ["-u", "user", "-c", "mycomputer", "-l", "data/log.csv"]
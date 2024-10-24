FROM python:3

WORKDIR /app

COPY . /app

ENTRYPOINT [ "sh", "-c", "if [ \"$RUN_TESTS\" = 'true' ]; then python -m unittest test.tests; else python src/main.py -u user -c mycomputer -l data/log.csv; fi" ]

CMD ["-u", "user", "-c", "mycomputer", "-l", "data/log.csv"]
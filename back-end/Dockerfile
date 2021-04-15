FROM python:3.8
RUN mkdir /flask_app
COPY . /flask_app/
WORKDIR /flask_app/src
EXPOSE 5000
RUN pip install -r requirements.txt
ENV FLASK_APP=main.py
ENV FLASK_ENV=development
RUN cp .env.example .env
CMD ["flask", "run", "-h", "0.0.0.0"]


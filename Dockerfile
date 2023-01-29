FROM python:3.8-slim
RUN pip install pulp flask numpy
COPY . app/
WORKDIR /app
EXPOSE 5000
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host", "0.0.0.0"]

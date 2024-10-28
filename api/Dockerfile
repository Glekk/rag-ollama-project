FROM python:3.10-slim

WORKDIR /project/api/

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN ls -la

EXPOSE 8080

CMD [ "python", "api.py" ]
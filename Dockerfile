FROM python:3.11

WORKDIR /app

COPY ships_full.json ships_full.json
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["./start_server.sh"]

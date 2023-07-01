FROM python:3.10-slim
WORKDIR /app
RUN chmod 755 .
COPY . .
RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir
CMD ["python", "main.py"]
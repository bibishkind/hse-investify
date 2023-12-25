# Dockerfile
FROM python
WORKDIR /api
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["alembic", "upgrade", "head", "&&", "python", "main.py"]
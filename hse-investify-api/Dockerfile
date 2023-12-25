# Dockerfile
FROM python
WORKDIR /api
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
VOLUME main.log:main.log
CMD ["alembic", "upgrade", "head", "&&", "python", "main.py"]
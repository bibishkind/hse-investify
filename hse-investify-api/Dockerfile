# Dockerfile
FROM python
WORKDIR /api
COPY . .
EXPOSE 8000
VOLUME ./main.log:main.log
RUN pip install -r requirements.txt
CMD sh -c "sleep 10; alembic upgrade head; python main.py"
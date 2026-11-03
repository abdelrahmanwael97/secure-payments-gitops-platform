FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

# Create a dedicated non-root user
RUN groupadd --system app && \
    useradd --system --gid app --create-home app

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application files with ownership assigned to app
COPY --chown=app:app src/ ./src/

# Run the application without root privileges
USER app

EXPOSE 8080

CMD ["uvicorn", "payment_api.main:app", "--host", "0.0.0.0", "--port", "8080"]

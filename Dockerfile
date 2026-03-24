FROM python:3.13-slim

# Install system dependencies for geopandas, psycopg2, and others
RUN apt-get update && apt-get install -y --no-install-recommends \
	build-essential \
	gcc \
	g++ \
	libpq-dev \
	libgeos-dev \
	libproj-dev \
	gdal-bin \
	&& rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
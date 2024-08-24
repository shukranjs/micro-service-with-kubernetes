FROM python:3.10-slim

WORKDIR /app

RUN pip install poetry

# Copy only the necessary files to install dependencies
COPY pyproject.toml poetry.lock /app/

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the rest of the application code into the container
COPY . /app/

# Expose the Flask port
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the application
CMD ["poetry", "run", "flask", "run"]

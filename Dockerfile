FROM python:3.11-slim-buster as builder

# Set environment variables
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VERSION=1.4.2
ENV PATH=$POETRY_HOME/bin:$PATH

# Create an isolated environment for Poetry and install it
RUN python -m venv $POETRY_HOME \
    && $POETRY_HOME/bin/pip install --no-cache-dir --upgrade pip \
    && $POETRY_HOME/bin/pip install --no-cache-dir "poetry==$POETRY_VERSION"

# Set the working directory for the project
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files (if they exist) into the container
COPY pyproject.toml poetry.lock* /app/

# Install project dependencies in the target environment
RUN poetry config virtualenvs.create true \
    && poetry config virtualenvs.in-project true \
    && poetry install --no-root

# Copy the rest of the application code into the container
COPY . /app

# Set the command to run your application using the target environment
CMD ["poetry", "run", "python", "dotsavvy/main.py"]

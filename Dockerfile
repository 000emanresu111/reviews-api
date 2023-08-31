FROM python:3.9

ENV DOCKER_ENV=True

WORKDIR /code

# Install Chrome
RUN apt-get install -y wget
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \ 
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get -y install google-chrome-stable

# Install ChromeDriver
RUN CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget -q -O /tmp/chromedriver_linux64.zip "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/116.0.5845.96/linux64/chromedriver-linux64.zip" && \
    unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin && \
    rm /tmp/chromedriver_linux64.zip

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:${PATH}"

# Configure poetry virtualenvs
RUN poetry config virtualenvs.in-project true

# Copy application files
COPY app /code/app
COPY README.md /code/README.md
COPY main.py /code/main.py
COPY pyproject.toml /code/pyproject.toml
COPY poetry.lock /code/poetry.lock
COPY Makefile /code/Makefile

# Install dependencies
RUN poetry install --no-dev

# Run application
CMD ["poetry", "run", "uvicorn", "main:app", "--port", "8086", "--host", "0.0.0.0"]

# Expose port
EXPOSE 8086

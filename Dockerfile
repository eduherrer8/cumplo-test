# I: Runtime Stage: ============================================================
# This is the stage where we build the runtime base image, which is used as the
# common ancestor by the rest of the stages, and contains the minimal runtime
# dependencies required for the application to run:

# 1. Start off from Python 3.6:
FROM python:3.6 AS runtime

# 2: Set the default workdir
WORKDIR /app

# 3: We'll set the workdir as HOME and add the app's executables path to $PATH:
ENV HOME=/app PATH=/app/bin:$PATH SASS_PROCESSOR_ENABLED=True

# 4: Ensure that Python outputs everything that's printed inside the application
# rather than buffering it:
ENV PYTHONUNBUFFERED 1

# 5: Install the common runtime dependencies:
RUN apt-get update && apt-get install -y --no-install-recommends \
 curl \
 libjpeg62-turbo \
 libpq5 \
 libopenblas-base \
 libssl1.1 \
 libxml2 \
 zlib1g \
 && rm -rf /var/lib/apt/lists/*

# II: Development Stage: =======================================================
# In this stage we'll build the image used for development, including compilers,
# and development libraries. This is also a first step for building a releasable
# Docker image:

# 1: Start off from the "runtime" stage:
FROM runtime AS development

# 2: Install the development dependencies from alpine package manager:
RUN apt-get update && apt-get install -y --no-install-recommends \
 build-essential \
 git \
 libjpeg62-turbo-dev \
 libpq-dev \
 libxml2-dev \
 python-dev \
 zlib1g-dev \
 && rm -rf /var/lib/apt/lists/*


# 3: Copy the requirements file:
COPY ./requirements.txt /app/

# 4: Fetch project dependencies:
RUN pip install -r requirements.txt

# III: Builder stage: ==========================================================
# In this stage we'll compile assets coming from the project's source, do some
# tests and cleanup. If the CI/CD that builds this image allows it, we should
# also run the app test suites here:

# 1: Start off from the "runtime" stage:
FROM development AS builder

# 2: Copy the rest of the app code:
COPY . /app

# 3: Compile SASS & collect the static files:
RUN rm -rf /app/static \
 && python manage.py collectstatic --noinput

# IV: Deployable stage: ========================================================
# In this stage, we build the final, deployable Docker image, which will be
# smaller than the images generated on previous stages:

# 1: Start off from the "runtime" stage:
FROM runtime AS deployable

# 2-5: We'll replicate the steps from "development" & "builder" stage so we use
# the most cached layers as possible:
WORKDIR /app
ENV HOME=/app PATH=/app/bin:$PATH SASS_PROCESSOR_ENABLED=True
ENV PYTHONUNBUFFERED 1
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl libjpeg62-turbo libpq5 libopenblas-base libssl1.1 libxml2 zlib1g \
 && rm -rf /var/lib/apt/lists/*

# 6: Copy the downloaded & compiled app dependencies from python builder:
COPY --from=builder /usr/local/lib/python3.6/site-packages /usr/local/lib/python3.6/site-packages

# 7: Copy the compiled app dependency executables from python builder:
COPY --from=builder /usr/local/bin /usr/local/bin

# 8: Copy the app code with collected static files from python builder:
COPY --from=builder /app /app

# 9: Set the default command - we set this last so we can cache the previous
# commands for other process types on Heroku:
CMD [ "uwsgi", "--ini", "/app/uwsgi.ini" ]

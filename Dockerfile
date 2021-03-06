# ------------------------------------------------------------------------------
# Description:
#    Dockerfile for the backend of 3duF.
#
# How to Use:
#     This is primarily intended to be run as part of a Github Actions workflow,
#     but it can be be built and run via the following commands:
#       docker build -t threeduf_backend .
#       docker run -it -d -p 80:80 threeduf_backend:latest
#
# Written by W.R. Jackson <wrjackso@bu.edu> on behalf of the DAMP Lab, 2021
# ------------------------------------------------------------------------------


FROM ubuntu:latest

ARG THREEDUF_ENV

# Set environment variables
ENV THREEDUF_ENV=${THREEDUF_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.0.0

############## System Level Dependencies ######################

# Install system level dependencies
RUN apt-get update
RUN apt install -y curl
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y nginx python3-pip git make build-essential python-dev libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev curl libffi-dev locate
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt install -y --fix-missing freecad-python3
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y freecad
RUN cp -a /usr/lib/freecad/Ext/. /usr/lib/freecad-python3/Ext/
RUN cp -a /usr/lib/freecad/Gui/. /usr/lib/freecad-python3/Gui/
RUN cp -a /usr/lib/freecad/Mod/. /usr/lib/freecad-python3/Mod/

# Pyenv for our baseline python environment for poetry later on.
RUN git clone git://github.com/yyuu/pyenv.git .pyenv
RUN git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv

ENV HOME  /
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH
ENV ENV_FILE_LOCATION=.env

RUN pyenv install 3.8.0
RUN pyenv global 3.8.0


# Install NPM to install our frontend...
RUN curl -sL https://deb.nodesource.com/setup_10.x -o nodesource_setup.sh
RUN bash nodesource_setup.sh
RUN apt install nodejs


WORKDIR /api

# Install our python dependency manager
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
COPY poetry.lock pyproject.toml /api/

# Project initialization:
WORKDIR /api
RUN poetry config virtualenvs.create false && poetry install $(if [ "$THREEDUF_ENV" == 'production' ]; then echo "--no-dev"; fi) --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . /api
# Generate JWT Key for the purposes of signing
RUN JWT_KEY=$(openssl rand -base64 172 | tr -d '\n') && echo "JWT_SECRET_KEY = \"${JWT_KEY}\"" >> .env
# Expose
EXPOSE 5000
# Run
RUN ls
CMD ["python", "app/app.py"]

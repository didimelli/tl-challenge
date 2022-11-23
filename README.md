# Software Engineer Challenge

The app spins up a rest api with the endpoints requested in the challenge pdf. At the route `/docs` there is a `Swagger UI`, while at `/redoc` there is an alternative documentation made with `redoc`.

The app has been developed with (modern) Python for simplicity and because I am familiar with the language and the ecosystem.

All the codebase is type hinted and leverages `async/await` for concurrency.

## How to run

### Docker

Once `Docker` is installed [on your system](https://docs.docker.com/engine/install/), just run:

```sh
docker build https://github.com/didimelli/tl-challenge.git#main -t tl-challenge && docker run -ti -p 8000:8000 tl-challenge
```

This will automatically fetch the repo and the `Dockerfile` from Github, build it (tagging it with `tl-challenge`) and run it.
The arguments after `docker run` are:

- `-ti`: to allow interactivity with the shell (easy kill with `Ctrl-c`)
- `-p 8000:8000`: the app listens to the port 8000. This binds the internal port 8000 to the host machine port 8000. User can change the host port with the second number after `:`.

### Python

This is a little trickier, since it requires to clone the repo, install Python and the dependencies.
To install python, [`pyenv`](https://github.com/pyenv/pyenv) is highly recommended since it ensures to have clean version management. **Please note that only Python 3.11 is supported**.
To install dependencies, both [`poetry`](https://github.com/python-poetry/poetry) and plain `pip + virtualenv` can be used. For development, I used `poetry`, but for a simple _clone and run_, it may be a little overkill, so `pip` is recommended.

To setup with `pip`, once the repo is cloned and python is installed:

```sh
# navigate to the repo
cd /path/to/repo/tl-challenge

# generate a virtualenv (in my case, python3.11 is the correct executable, it might slightly change based on your installation method.) in a folder called .venv
python3.11 -m venv .venv

# use the virtualenv python to install dependencies
.venv/bin/python -m pip install -r requirements.txt
# Ignoring colorama: markers 'python_version >= "3.8" and python_version < "4.0" and platform_system == "Windows"' don't match your environment
# Collecting anyio==3.6.2
#   Downloading anyio-3.6.2-py3-none-any.whl (80 kB)
#      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 80.6/80.6 kB 1.5 MB/s eta 0:00:00
# ... OUTPUT CROPPED ...

# start the app. This will start the app listening to localhost on port 8000
.venv/bin/uvicorn tl_challenge.app:app
# INFO:     Started server process [158057]
# INFO:     Waiting for application startup.
# INFO:     Application startup complete.
# INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

## Design decisions

The app structure is the following:

```sh
tl_challenge
├── __init__.py  # compulsory python file to make a module
├── app.py  # application logic
└── models.py  # api models
```

It is very simple and small. In `app.py` there is application logic, so endpoints and integration with 3rd party APIs are there.
In `models.py` there are the two main models returned by the api, one for the basic info, the other one with the information about the status of the translation.

For the `translated` endpoint, since the requirement asked to return the original description in the case the translation failed, I decided to add a `translated bool` field to the response, so that the user is aware that the translation actually did not happen.

Even if the requirements were simple, I tried to keep a clean code structure, with model logic detached from the app logic.

The app is only tested with Python 3.11 and it has been developed with that constraint. Since this is a service and not a library, compatibility with other _live_ python versions is not a requirement.

### Tests

There are a couple of tests for each endpoint, testing good or bad response from the 3rd party api.
They can be run after having installed the dev dependencies with:

```sh
# install dev dependencies
.venv/bin/python -m pip install -r requirements-dev.txt
# run tests. add --cod=tl_challenge to get coverage
.venv/bin/pytest  # --cov=tl_challenge
```

### Code quality

In `.pre-commit-config.yaml` there are defined hooks that assures that the code is properly formatted and linted before committing.

A simple `ci` with automated tests is implemented with `Github actions` (`.github/workflows/ci.yml`)

## Design decisions - Production

For a production api I would have done:

- HTTPS
- Rate limiting
- Caching: requesting `diglett` twice would call the pokeapi `twice`, yielding the same exact answer.
- Proper deployment on some _managed_ infrastructure, like Kubernetes or some container runner (like GCP Cloud Run), or at least with Systemd services on some cloud VM.
- Automatic deploy from CI
- More extensive tests: test every possible negative 3rd party response

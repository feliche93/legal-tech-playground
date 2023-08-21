# Court Judgement Prediction

## Creating a virtual environment

```bash
python3 -m venv venv
```

OR with pyenv:

```bash
pyenv virtualenv 3.11.1 court-judgement-prediction
```

## Installing dependencies

First install pip-tools:

```bash
pip install pip-tools
```

Then generate the required requirements.txt files:

```bash
pip-compile requirements.in -o requirements.txt
pip-compile requirements-dev.in -o requirements-dev.txt
```

Finally install the dependencies:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

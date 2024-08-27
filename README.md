# MultiagentesAPI

## Introduction

Django application that utilizes the MESA framework to simulate multiagent interactions.

Crafted by:

- Emilio Domínguez
- Marco Lucio
- Gabriel Mujica
- Leonardo Pequeño
- Saul Delgado

## Setup

Before running, you should make sure you have this packages installed in your preferred environment:

```
Django==4.2.15
Mesa==2.3.2
numpy==1.25.2
pandas==2.1.0
scipy==1.10.1
matplotlib==3.7.1
gunicorn==20.1.0
python-decouple==3.7
```

## Usage

In order to run local server, run this commands:

If not already in MultiagentesAPI/multiagentsapi <br>
```cd multiagentsapi```

Then <br>
```python manage.py runserver```

If that doesn't work, try: <br>
```python3 manage.py runserver```


For development purposes, you can modify multiagentsapi/settings.py in order to set ```Debug = True```, so that you get more information on errors. Nevertheless, don't push any code to main with that setting on.


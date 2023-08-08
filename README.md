# Ooti Test

Welcome to the documentation for the Ooti Test project! This guide will help you set up and run the project on your local machine.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running the Project](#running-the-project)
5. [Usage](#usage)
6. [Testing](#testing)
7. [Contributing](#contributing)
8. [License](#license)

## Prerequisites

Before you start, make sure you have the following tools installed:

- [Python](https://www.python.org/downloads/) (3.6 or later)
- [pip](https://pip.pypa.io/en/stable/installing/)

## Installation

1. Clone the repository:
git clone ```https://github.com/axoneprohr/ooti_test.git```
```cd ooti_test```

2. Install project dependencies:
```pip install -r requirements.txt```

## Configuration

1. Open `ooti_test/settings.py` and configure database settings, email settings, and any other settings specific to your project.

## Running the Project

1. Apply migrations:

```python manage.py migrate```

2. Create a superuser:

```python manage.py createsuperuser```

3. Start the development server:

```python manage.py runserver```

4. Access the admin panel at `http://127.0.0.1:8000/admin/` and use the superuser credentials.

## Usage

- Visit the home page at ```http://127.0.0.1:8000/```
- Use the provided forms and features to interact with the project.

## Testing

1. Run tests to ensure everything is working:

```python manage.py test wiki_stats```

# Ooti Test

Welcome to the documentation for the Ooti Test project! This guide will help you set up and run the project on your local machine.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running the Project](#running-the-project)
5. [Usage](#usage)
6. [Testing](#testing)

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

1. **Visit the Home Page:**
   Access the home page of the project by navigating to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your web browser. This is where you'll find the main interface of the application.

2. **Interact with the Provided Features:**
   Utilize the features and forms provided on the home page to interact with the project. You can perform actions like submitting queries, fetching data, and analyzing results.

3. **Fetching Data via URLs:**
   For developers familiar with APIs, you can also fetch data programmatically by sending GET requests to specific URLs. For example, to retrieve an analysis for a specific title, you can use a URL like:
   ```http://127.0.0.1:8000/api/extract-analysis/?title=YourTitleHere```
   Replace `YourTitleHere` with the desired title you want to analyze.

## Testing

1. Run tests to ensure everything is working:

```python manage.py test wiki_stats```

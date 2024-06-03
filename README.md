# Django + Scrapy Project

This project integrates Django with Scrapy to build a web application that scrapes computer product data from `desktop.bg` and displays it via a REST API. The scraped data is stored in a SQLite database, and users can query the data through a Django-based web interface.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the Scrapy Spider](#running-the-scrapy-spider)
  - [Querying the Data](#querying-the-data)
- [File Structure](#file-structure)
- [Endpoints](#endpoints)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

The project consists of a Django web application and a Scrapy spider. The spider scrapes data from `desktop.bg`, specifically computer product details like processor, GPU, motherboard, and RAM. This data is stored in a SQLite database. The Django application provides an API for scraping new data and querying the stored data.

## Features

- **Web Scraping**: Scrapy spider to scrape computer product data from `desktop.bg`.
- **Data Storage**: Scraped data is stored in a SQLite database.
- **REST API**: Django views to trigger the scraping process and to query the scraped data.

## Installation

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/DonkoTonev/django-scrapy-project.git
   cd django-scrapy-project
   ```

2. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

3. **Apply Migrations**:
   ```sh
   python manage.py migrate
   ```

4. **Run the Django Development Server**:
   ```sh
   python manage.py runserver
   ```

## Usage

### Running the Scrapy Spider

To start the web scraping process, navigate to the following endpoint in your browser:

```sh
http://127.0.0.1:8000/scrape-desktop-bg/
```


This will trigger the Scrapy spider to start scraping data from `desktop.bg`. Once the process is completed, a success or failure message will be returned.

### Querying the Data

To query the scraped data, you can use the following endpoint with optional query parameters for filtering:

```sh
http://127.0.0.1:8000/computers/?processor=Intel&gpu=NVIDIA
```

This will return a JSON response with the computer products that match the specified criteria.

## File Structure

```sh
myproject/
├── myproject/
│ ├── __init__.py
│ ├── asgi.py
│ ├── settings.py
│ ├── urls.py
│ ├── views.py
│ ├── wsgi.py
├── scrapers/
│ ├── migrations/
│ │ └── __init__.py
│ ├── spiders/
│ │ └── desktop_spider.py
│ ├── __init__.py
│ ├── admin.py
│ ├── apps.py
│ ├── models.py
│ ├── tests.py
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md
```


- **spiders/desktop_spider.py**: Scrapy spider for scraping `desktop.bg`.
- **myproject/views.py**: Django views for scraping and querying data.
- **myproject/urls.py**: URL routing for the Django application.

## Endpoints

### Scraping Endpoint

- **URL**: `/scrape-desktop-bg/`
- **Method**: GET
- **Description**: Triggers the Scrapy spider to scrape data from `desktop.bg`.

### Query Endpoint

- **URL**: `/computers/`
- **Method**: GET
- **Description**: Returns a list of computer products. Supports optional query parameters:
  - `processor`
  - `gpu`
  - `motherboard`
  - `ram`

Example:

```sh
http://127.0.0.1:8000/computers/?processor=Intel&gpu=NVIDIA
```


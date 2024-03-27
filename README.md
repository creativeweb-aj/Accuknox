# Social Network App for Accuknox

## Introduction

This project is a social networking application developed for Accuknox. It comes with a Postman collection for easy API testing and interaction.

## Prerequisites

Before you begin, ensure you have Python 3.9.6 installed on your system. If you do not have Python installed, you can download it from [python.org](https://www.python.org/downloads/).

## Setup Instructions

### 1. Clone the Repository

Start by cloning the repository to your local machine. Open a terminal and run the following command:

git clone `<repository-url>`

Replace `<repository-url>` with the actual URL of the repository.

### 2. Create a Virtual Environment

Navigate into the project directory:
cd path/to/cloned/repo

Create a virtual environment using Python 3.9.6:
python3.9 -m venv env


Activate the virtual environment:

- On Windows:
env\Scripts\activate
- On macOS and Linux:
source env/bin/activate


### 3. Install Dependencies

Install all the required packages from the `requirements.txt` file:

`pip install -r requirements.txt`


### 4. Environment Variables

Copy the content from the `example.env` file to a new file named `.env` in the project's root directory. This file should contain your database and secret key configurations. Update the `.env` file with your database details:

DATABASE_NAME=accuknox_db

DATABASE_USER=postgres

DATABASE_PASSWORD=12345

DATABASE_HOST=localhost

DATABASE_PORT=5432


### 5. Database Migrations

Apply the Django model migrations to create the necessary database tables:

`python manage.py migrate`


### 6. Run the Development Server

Finally, start the Django development server:

`python manage.py runserver 0.0.0.0:8001`


The application will now be running and accessible at `http://0.0.0.0:8001`.

### 7. Postman Collection

The project includes a Postman collection in `postman` folder that contains all the APIs you can use to interact with the application.


Once imported, you can start testing the APIs using the predefined requests.

## Conclusion

You have successfully set up the Social Network App for Accuknox on your local development environment. For further customization and development, refer to the project documentation.

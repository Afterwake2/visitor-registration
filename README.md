# Visitor Registration System

Simple visitor registration system using:

- Flask
- PostgreSQL 18
- Docker
- Docker Compose

## Features

- Visitor registration form
- PostgreSQL database storage
- Docker container deployment
- Simple UI

## Fields

- First Name
- Last Name
- Contact Number
- Company Name
- Purpose of Visit
- Contact Person

## Run the system

Clone the repository

git clone https://github.com/YOURUSERNAME/visitor-registration.git

cd visitor-registration

Start containers

docker compose up -d --build

Open browser

http://localhost:5000

## Database

PostgreSQL 18 container.

Table: visitors

Columns:

- first_name
- last_name
- contact_number
- company_name
- purpose_of_visit
- contact_person
- visit_time
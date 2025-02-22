# health_monitoing_system

# Health Tracker API

## Overview

The **Health Tracker API** is a FastAPI-based application designed to manage and track users' health-related data, including activities, sleep records, test results, and more. It provides RESTful API endpoints for storing, retrieving, updating, and deleting health-related records.

This project is designed to be run **locally** (without Docker).

---

## Features

- User Management (Create, Retrieve, Update, Delete)
- Health Metrics Tracking (Activities, Steps, Sleep, Test Results)
- FastAPI for lightweight and high-performance REST API
- PostgreSQL as the database
- SQLAlchemy with async support for efficient database operations
- Automatic database initialization and migrations

---

## API Endpoints

### Users API

| Method | Endpoint         | Description                 |
|--------|----------------|-----------------------------|
| `POST` | `/users/`      | Create a new user          |
| `GET`  | `/users/{id}`  | Get user by ID             |
| `PUT`  | `/users/{id}`  | Update user details        |
| `DELETE` | `/users/{id}` | Delete a user              |

### Activities API

| Method | Endpoint          | Description                   |
|--------|------------------|-------------------------------|
| `POST` | `/activities/`   | Create an activity           |
| `GET`  | `/activities/`   | Get all activities           |
| `GET`  | `/activities/{id}` | Get activity by ID          |
| `PUT`  | `/activities/{id}` | Update an activity         |
| `DELETE` | `/activities/{id}` | Delete an activity       |

### Sleep API

| Method | Endpoint        | Description                |
|--------|--------------|----------------------------|
| `POST` | `/sleep/`   | Log sleep data            |
| `GET`  | `/sleep/`   | Get all sleep records     |
| `GET`  | `/sleep/{id}` | Get sleep record by ID   |
| `PUT`  | `/sleep/{id}` | Update sleep record      |
| `DELETE` | `/sleep/{id}` | Delete sleep record    |

### Test Results API

| Method | Endpoint           | Description                  |
|--------|-------------------|------------------------------|
| `POST` | `/test-results/`  | Create a test result        |
| `GET`  | `/test-results/`  | Get all test results        |
| `GET`  | `/test-results/{id}` | Get test result by ID  |
| `PUT`  | `/test-results/{id}` | Update test result     |
| `DELETE` | `/test-results/{id}` | Delete test result   |

---

## Database Schema

### Tables

#### Users
- `id` (Primary Key)
- `first_name`
- `last_name`
- `email`
- `dob`
- `gender`
- `height`
- `weight`
- `created_at`

#### Activities
- `id` (Primary Key)
- `user_id` (Foreign Key)
- `activity_type`
- `start_time`
- `end_time`
- `calories_burned`
- `created_at`

#### Sleep Records
- `id` (Primary Key)
- `user_id` (Foreign Key)
- `sleep_date`
- `sleep_duration`
- `sleep_efficiency`
- `deep_sleep_min`
- `rem_sleep_min`
- `wakeups`
- `bedtime`
- `wake_time`
- `created_at`

#### Test Results
- `id` (Primary Key)
- `user_id` (Foreign Key)
- `test_type`
- `result_value`
- `test_date`
- `created_at`

---

## Installation and Setup

### Prerequisites
- Python 3.10+
- PostgreSQL Database

### Steps to Run Locally

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-repo/health-tracker-api.git
   cd health-tracker-api

# Reviews_assignment

Problem Statement : 
This project is a FastAPI-based application for managing and analyzing review trends using PostgreSQL and Redis. It includes:

APIs for retrieving top review categories based on average star ratings.

Logging of API activity using Celery and Redis.

Asynchronous task execution with Celery workers.

My Understanding:
For creating above features, I have first created data required for testing. So I created 15 categoreis and 200 review history records as per the problem statement requirement which will cover most of testcases. Now I pushed the created data in my postgre sql online instance and created apis and tested them. 

Technologies Used:
FastAPI - Web framework for API development.
PostgreSQL - Relational database for storing review data.
Redis - Used as a caching mechanism and log storage.
SQLAlchemy - ORM for database interaction.
Celery - Task queue for asynchronous logging.

Prerequisites:
Python 3.12
FastAPI
SqlAlchemy Orm
Celery 
PostgreSQL database (serverless instance recommended)
Redis (serverless instance recommended)

Steps to Run Locally
1. Clone the Repository
$ git clone <repo-url>
$ cd reviews-api

2. Create and Activate Virtual Environment
$ python -m venv venv
$ source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install Dependencies
$ pip install -r requirements.txt

4. Set the respective urls in database.py & redisdb.py with the following details:
DATABASE_URL=postgresql://user:password@host:port/dbname
REDIS_URL=rediss://user:password@host:port

5. Run the FastAPI Server
$ uvicorn app.main:app --reload

6. Start Celery Worker
$ celery -A app.celery_config worker --loglevel=info

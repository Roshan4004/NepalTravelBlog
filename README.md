# Celery App for Asynchronous Task Scheduling

This repository branch contains a separate Celery application specifically for handling background tasks, independent from the main Django application. While the Django app manages web requests, the Celery app is focused on the AI blog generation.

## Why Separate Celery from Django?

1. **Performance**: By separating Celery from Django, we allow the web server to remain responsive while Celery handles long-running tasks in the background.
2. **Scalability**: This separation allows both the Django and Celery services to scale independently, adapting to their respective workloads.

## Running the Celery App Using Docker

There are two ways to run the Celery app using Docker:

### Option 1: Pull and Run the Docker Image from Docker Hub

1. **Pull the image**:
   ```bash
   docker pull roshan4004/celery-api-caller:latest
   ```
   Then, continue with creating continer and then running.


### Option 2: Build the Image Locally and Run It

1. **Clone the repository**:
   ```bash
   git clone -b celery_seperate https://github.com/your-repo.git
   cd your-repo
   ```

2. **Build the Docker image**:
   ```bash
   docker-compose up --build
   ```


### Environment Configuration

Make sure to create an `.env` file with the following configurations:

```bash
REDIS_URL=redis://:password@hostname:port/0
# Other environment variables required for the Celery app
```

## Notes

- Ensure the Redis service is up and running, as Celery relies on Redis to manage task queues.
- For development purposes, you can add a shared network with the Django app to simulate production environments, ensuring communication between Celery and Django.


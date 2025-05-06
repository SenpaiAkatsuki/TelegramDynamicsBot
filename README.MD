# TelegramDynamicsBot

TelegramDynamicsBot is a modern solution for automating Telegram group announcements by combining two key components into one integrated system.

---

## Components

### Main Telegram Bot
- **Framework:** [Aiogram](https://docs.aiogram.dev/)
- **Role:** Provides an intuitive interface for administrators to create, schedule, and manage announcements, groups, and message templates.
- **Features:** 
  - Command handling
  - Interactive dialogues for setup and management
  - Real-time status monitoring

### Userbot (Message Dispatcher)
- **Framework:** [Pyrogram](https://docs.pyrogram.org/)
- **Role:** Logs in as a Telegram user to bypass Bot API restrictions and dispatch scheduled messages to groups.
- **Features:**
  - Scheduled message dispatch using [APScheduler](https://apscheduler.readthedocs.io/)
  - Seamless integration with the main bot via a shared database

---

## Key Features

- **Dual-Component Architecture:**  
  Separates administrative functions from message dispatching for enhanced scalability and flexibility.

- **Robust Data Management:**  
  Utilizes PostgreSQL with [SQLAlchemy](https://www.sqlalchemy.org/) for ORM and [Alembic](https://alembic.sqlalchemy.org/) for database migrations.

- **Containerized Deployment:**  
  Fully Dockerized using Docker Compose, including containers for:
  - Main bot
  - Userbot
  - PostgreSQL
  - Redis (optional)
  - Adminer for database management

- **Modern Asynchronous Stack:**  
  Leverages Python 3.10+ with asynchronous libraries to handle multiple tasks efficiently.

---

## Technologies

- **Language:** Python 3.10+
- **Frameworks & Libraries:**
  - **Aiogram:** For Telegram Bot API interactions.
  - **Pyrogram:** For Telegram client operations.
  - **SQLAlchemy & Alembic:** For ORM and database migrations.
  - **APScheduler:** For task scheduling.
  - **Docker:** For containerization.
- **Database & Caching:**
  - **PostgreSQL:** Primary data storage.
  - **Redis:** Optional, for caching and state management.

# First Setup.

1. `docker-compose up`
   It will create the containers.
2. `CTRL + Z`
   It will detach from the containers.
3. `sh run_migrations.sh`
   It will run the migrations for the DB.

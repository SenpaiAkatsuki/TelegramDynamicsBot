read -p "Enter name of migration: " message && docker exec telegram_dynamic_bot alembic revision --autogenerate -m "$message"

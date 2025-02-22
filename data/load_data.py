import sys
import os

# Ensure Python finds `app/` as a module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import asyncio
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.logger import logging
from db.database import AsyncSessionLocal
from db.models import GenderEnum, User, Test, TestResult, SleepingActivity, DailySteps, ActivityType, PhysicalActivity


# Load JSON data from files
def load_json_data(filename):
    with open(os.path.join(os.getcwd(), "data", filename), "r") as file:
        return json.load(file)


# Convert date string to datetime.date
def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").date()


# Insert Users
async def insert_users(db: AsyncSession):
    users = load_json_data("users.json")

    for user in users:
        user["dob"] = parse_date(user["dob"])  # ✅ Convert to datetime.date
        user["gender"] = GenderEnum(user["gender"].capitalize())  # ✅ Convert to correct case

    db.add_all([User(**user) for user in users])
    await db.commit()


# Insert Tests
async def insert_tests(db: AsyncSession):
    tests = load_json_data("tests.json")
    db.add_all([Test(**test) for test in tests])
    await db.commit()


# Insert Test Results
async def insert_test_results(db: AsyncSession):
    test_results = load_json_data("test_results.json")

    for result in test_results:
        result["test_date"] = parse_date(result["test_date"])  # ✅ Convert to datetime.date

    db.add_all([TestResult(**result) for result in test_results])
    await db.commit()


# Insert Sleeping Activity
async def insert_sleep_data(db: AsyncSession):
    sleep_data = load_json_data("sleep.json")
    for sleep in sleep_data:
        sleep["sleep_date"] = parse_date(sleep["sleep_date"])  # ✅ Convert to datetime.date
        sleep["bedtime"] = datetime.fromisoformat(sleep["bedtime"])  # ✅ Convert to datetime
        sleep["wake_time"] = datetime.fromisoformat(sleep["wake_time"])  # ✅ Convert to datetime
    db.add_all([SleepingActivity(**sleep) for sleep in sleep_data])
    await db.commit()


# Insert Daily Steps
async def insert_daily_steps(db: AsyncSession):
    steps_data = load_json_data("daily_steps.json")

    for step in steps_data:
        step["date"] = parse_date(step["date"])  # ✅ Convert to datetime.date

    db.add_all([DailySteps(**step) for step in steps_data])
    await db.commit()


# Insert Activity Types
async def insert_activity_types(db: AsyncSession):
    activity_types = load_json_data("activity_types.json")
    db.add_all([ActivityType(**activity) for activity in activity_types])
    await db.commit()


# Insert Physical Activities
async def insert_physical_activity(db: AsyncSession):
    activity_data = load_json_data("activities.json")

    for activity in activity_data:
        activity["start_time"] = datetime.fromisoformat(activity["start_time"])  # ✅ Convert to datetime
        activity["end_time"] = datetime.fromisoformat(activity["end_time"])  # ✅ Convert to datetime

    db.add_all([PhysicalActivity(**activity) for activity in activity_data])
    await db.commit()


# Run all insert operations
async def insert_all_data(session: AsyncSession):
    await insert_users(session)
    await insert_tests(session)
    await insert_activity_types(session)
    await insert_test_results(session)
    await insert_sleep_data(session)
    await insert_daily_steps(session)
    await insert_physical_activity(session)
    logging.info("✅ Data insertion complete!")


# Main function to run the script
async def main():
    logging.info("⏳ Starting data insertion...")
    async with AsyncSessionLocal() as session:
        await insert_all_data(session)
        await session.commit()
    logging.info("✅ Data insertion completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())

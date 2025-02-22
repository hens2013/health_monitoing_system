from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Date, TIMESTAMP, Enum, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base import Base
import enum


class GenderEnum(str, enum.Enum):
    Male = "Male"
    Female = "Female"
    Other = "Other"


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    dob = Column(Date, nullable=False)
    gender = Column(Enum(GenderEnum, name="gender_enum"), nullable=False)
    height = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.now)

    __table_args__ = (
        Index("idx_users_email", email),
        Index("idx_users_dob", dob),
    )


# Tests Table
class Test(Base):
    __tablename__ = "tests"
    test_id = Column(Integer, primary_key=True, autoincrement=True)
    test_name = Column(String, nullable=False)
    unit = Column(String, nullable=False)
    lower_bound = Column(Float, nullable=False)
    upper_bound = Column(Float, nullable=False)


# Test Results Table
class TestResult(Base):
    __tablename__ = "test_results"
    result_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    test_id = Column(Integer, ForeignKey("tests.test_id", ondelete="CASCADE"), nullable=False)
    test_date = Column(DateTime, nullable=False)
    result_value = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    test = relationship("Test", backref="test_results", lazy="joined")

    __table_args__ = (
        Index("idx_test_results_user", user_id),
        Index("idx_test_results_test", test_id),
        Index("idx_test_results_date", test_date),
    )


# Sleeping Activity Table
class SleepingActivity(Base):
    __tablename__ = "sleeping_activity"
    sleep_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    sleep_date = Column(DateTime, nullable=False)
    sleep_duration = Column(Integer, nullable=False)
    sleep_efficiency = Column(Float, nullable=False)
    deep_sleep_min = Column(Integer, nullable=False)
    rem_sleep_min = Column(Integer, nullable=False)
    wakeups = Column(Integer, nullable=False)
    bedtime = Column(DateTime, nullable=False)
    wake_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    __table_args__ = (
        Index("idx_sleep_user", user_id),
        Index("idx_sleep_date", sleep_date),
    )


# Daily Steps Table
class DailySteps(Base):
    __tablename__ = "daily_steps"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    date = Column(DateTime, nullable=False)
    total_steps = Column(Integer, nullable=False)
    total_calories_burned = Column(Float, nullable=True)
    distance_walked_km = Column(Float, nullable=True)
    active_minutes = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    __table_args__ = (
        Index("idx_daily_steps_user", user_id),
        Index("idx_daily_steps_date", date),
    )


# Activity Types Table
class ActivityType(Base):
    __tablename__ = "activity_types"
    activity_type_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)


# Physical Activity Table
class PhysicalActivity(Base):
    __tablename__ = "physical_activity"
    activity_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    activity_type_id = Column(Integer, ForeignKey("activity_types.activity_type_id", ondelete="CASCADE"),
                              nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    calories_burned = Column(Float, nullable=True)
    avg_heart_rate = Column(Integer, nullable=True)
    max_heart_rate = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    __table_args__ = (
        Index("idx_activity_user", user_id),
        Index("idx_activity_type", activity_type_id),
        Index("idx_activity_time", start_time, end_time),
    )

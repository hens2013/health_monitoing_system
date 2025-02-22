# Health Score Calculations
from sqlalchemy.ext.asyncio import AsyncSession

# Import Services
from db.cruds.user_crud import user_service
from db.cruds.test_results_crud import test_result_service
from db.cruds.daily_steps_crud import step_service
from db.cruds.sleep_activity_crud import sleep_service
from db.cruds.activity import activity_service
from db.database import AsyncSessionLocal
from app.utils.helper_functions import calculate_age
from app.utils.pdf import PDFReport

IDEAL_SLEEP_HOURS = 8
TARGET_STEPS = 10000
TARGET_ACTIVE_MINUTES = 60
TARGET_CALORIES = 2500


def calculate_BHI(test_results):
    if not test_results:
        return 100

    score = 100
    for test in test_results:
        if not test.test or test.test.lower_bound is None or test.test.upper_bound is None:
            continue

        lower = test.test.lower_bound
        upper = test.test.upper_bound
        deviation = abs(test.result_value - ((lower + upper) / 2))
        if test.result_value < lower or test.result_value > upper:
            score -= deviation * 0.5

    return score


def calculate_AHS(steps, activities):
    """
    Calculates the Activity-Based Health Score (AHS).
    - Uses total steps, active minutes, and calories burned.
    - Normalizes to avoid an AHS of always 100.
    """

    total_steps = sum([s.total_steps for s in steps]) if steps else 0
    active_minutes = sum([(a.end_time - a.start_time).total_seconds() // 60 for a in activities]) if activities else 0
    calories_burned = sum([a.calories_burned for a in activities]) if activities else 0

    # Prevent division by zero and normalize to 100
    step_score = (total_steps / TARGET_STEPS) if TARGET_STEPS else 0
    activity_score = (active_minutes / TARGET_ACTIVE_MINUTES) if TARGET_ACTIVE_MINUTES else 0
    calorie_score = (calories_burned / TARGET_CALORIES) if TARGET_CALORIES else 0

    # Ensure values are in the range 0-1 before applying weights
    step_score = min(1, step_score)
    activity_score = min(1, activity_score)
    calorie_score = min(1, calorie_score)

    # Compute weighted AHS
    AHS = (step_score * 40) + (activity_score * 30) + (calorie_score * 30)

    return round(AHS, 2)  # Return rounded score


def calculate_SQS(sleep_activities):
    if not sleep_activities:
        return 50

    total_sleep_hours = sum([s.sleep_duration / 60 for s in sleep_activities]) / len(sleep_activities)
    score = 100 - (abs(IDEAL_SLEEP_HOURS - total_sleep_hours) * 10)
    return max(0, min(100, score))


def calculate_FHS(BHI, AHS, SQS, weights=None):
    if weights is None:
        weights = {"BHI": 0.4, "AHS": 0.3, "SQS": 0.3}

    total_weight = sum(weights.values())
    if total_weight != 1:
        weights = {key: value / total_weight for key, value in weights.items()}

    final_score = (
        weights["BHI"] * BHI +
        weights["AHS"] * AHS +
        weights["SQS"] * SQS
    )
    return round(final_score, 2)


async def fetch_user_health_data(user_id: int, db: AsyncSession):
    user = await user_service.get_by_id(db, user_id)
    if not user:
        return None

    age = calculate_age(user.dob)
    user_tests = await test_result_service.get_by_user_id(db, user_id)
    user_steps = await step_service.get_by_user_id(db, user_id)
    user_sleep = await sleep_service.get_by_user_id(db, user_id)
    user_activities = await activity_service.get_by_user_id(db, user_id)

    return {
        "user": user,
        "age": age,
        "test_results": user_tests,
        "steps": user_steps,
        "sleep": user_sleep,
        "activities": user_activities,
    }


async def generate_pdf_report(user_id: int):
    async with AsyncSessionLocal() as db:
        user_data = await fetch_user_health_data(user_id, db)

    if not user_data:
        print(f"User ID {user_id} not found.")
        return

    user = user_data["user"]
    BHI = calculate_BHI(user_data["test_results"])
    AHS = calculate_AHS(user_data["steps"], user_data["activities"])
    SQS = calculate_SQS(user_data["sleep"])
    FHS = calculate_FHS(BHI, AHS, SQS)

    pdf = PDFReport()
    pdf.add_page()

    pdf.add_section("User Details",
                    f"Name: {user.first_name} {user.last_name}\n"
                    f"Age: {user_data['age']}\n"
                    f"Gender: {str(user.gender).split('.')[-1]}\n"
                    f"Height: {user.height} cm\n"
                    f"Weight: {user.weight} kg")

    if BHI < 0:
        warning = "🚨 Severe health issues detected! Seek medical attention."
    elif BHI < 50:
        warning = "⚠️ Multiple health deviations detected. Consider visiting a doctor."
    else:
        warning = "✅ Health biometrics within a good range."

    pdf.add_section("Test Results", warning)
    pdf.add_section("Daily Activity",
                    f"Total Steps: {sum([s.total_steps for s in user_data['steps']])}\n"
                    f"Active Minutes: {sum([(a.end_time - a.start_time).total_seconds() // 60 for a in user_data['activities']])}\n"
                    f"Calories Burned: {sum([a.calories_burned for a in user_data['activities']])}")

    avg_sleep = sum([s.sleep_duration for s in user_data["sleep"]]) / len(user_data["sleep"]) if user_data[
        "sleep"] else "N/A"
    pdf.add_section("Sleep Data",
                    f"Average Sleep Duration: {avg_sleep} hours")

    pdf.add_section("Health Scores",
                    f"BHI: {BHI:.2f}\n"
                    f"AHS: {AHS:.2f}\n"
                    f"SQS: {SQS:.2f}\n"
                    f"Final Health Score (FHS): {FHS:.2f}")

    file_path = f"health_report_user_{user_id}.pdf"
    pdf.output(file_path)
    print(f"Report saved as {file_path}")

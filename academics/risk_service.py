import os
import joblib
import pandas as pd

MODEL_DIR = os.path.join(os.path.dirname(__file__), "ml")
_model = joblib.load(os.path.join(MODEL_DIR, "risk_model.joblib"))
_feature_columns = joblib.load(os.path.join(MODEL_DIR, "feature_columns.joblib"))


def build_features_for_student(student):
    from academics.models import Enrollment, AttendanceRecord

    enrollments = Enrollment.objects.filter(student=student)

    marks_data = []
    for e in enrollments:
        for m in e.marks.all():
            marks_data.append(float(m.score_percent))
    average_mark = sum(marks_data) / len(marks_data) if marks_data else 0

    attendance_qs = AttendanceRecord.objects.filter(enrollment__student=student)
    total_records = attendance_qs.count()
    attendance_rate = (
        attendance_qs.filter(present=True).count() / total_records * 100
        if total_records else 100
    )

    modules_failed_count = enrollments.filter(status="failed").count()
    module_retakes = 0

    profile = student.student_profile
    credits_completed = profile.credits_completed
    credits_required_to_date = profile.credits_required

    submission_rate = attendance_rate
    study_hours_per_week = 10
    is_distance_learner = 0

    return pd.DataFrame([{
        "average_mark": average_mark,
        "attendance_rate": attendance_rate,
        "submission_rate": submission_rate,
        "modules_failed_count": modules_failed_count,
        "module_retakes": module_retakes,
        "credits_completed": credits_completed,
        "credits_required_to_date": credits_required_to_date,
        "study_hours_per_week": study_hours_per_week,
        "is_distance_learner": is_distance_learner,
    }])[_feature_columns]


ADVICE_TEMPLATES = {
    "high": "You're currently at high academic risk. Focus first on the module(s) "
            "with the lowest marks, and book time with your lecturer or academic "
            "advisor this week — don't wait for the next assessment to fix this.",
    "medium": "You're at medium risk — a few areas need attention before they "
              "become bigger problems. Review your lowest-performing module and "
              "increase your weekly study time if you can.",
    "low": "You're on track. Keep up your current attendance and submission habits.",
}


def predict_risk_for_student(student):
    features = build_features_for_student(student)
    risk_level = _model.predict(features)[0]
    advice_text = ADVICE_TEMPLATES[risk_level]
    return risk_level, advice_text, features.iloc[0].to_dict()

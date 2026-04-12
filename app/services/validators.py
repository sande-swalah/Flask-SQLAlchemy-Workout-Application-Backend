VALID_CATEGORIES = [
    "strength",
    "cardio",
    "flexibility",
    "balance",
    "plyometrics",
    "other",
]


def validate_name(value):
    if value is None or not str(value).strip():
        raise ValueError("Exercise name cannot be blank.")
    return str(value).strip()


def validate_category(value):
    if value not in VALID_CATEGORIES:
        raise ValueError(
            f"Category must be one of: {', '.join(VALID_CATEGORIES)}."
        )
    return value


def validate_duration_minutes(value):
    if value is None or int(value) <= 0:
        raise ValueError("Duration must be a positive integer (minutes).")
    return int(value)


def validate_date(value):
    if value is None:
        raise ValueError("Date is required.")
    return value


def validate_optional_positive_int(value, field_name):
    if value is None:
        return None

    numeric_value = int(value)
    if numeric_value <= 0:
        raise ValueError(f"{field_name} must be a positive integer.")
    return numeric_value


def validate_reps(value):
    return validate_optional_positive_int(value, "Reps")


def validate_sets(value):
    return validate_optional_positive_int(value, "Sets")


def validate_duration_seconds(value):
    return validate_optional_positive_int(value, "Duration (seconds)")
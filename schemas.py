from marshmallow import Schema, fields, validate, validates, ValidationError, post_load
from models import VALID_CATEGORIES
 
 


class ExerciseSummarySchema(Schema):
    """Lightweight exercise summary embedded inside WorkoutExercise."""
    id = fields.Int(dump_only=True)
    name = fields.Str(dump_only=True)
    category = fields.Str(dump_only=True)
    equipment_needed = fields.Bool(dump_only=True)
 
 
class WorkoutSummarySchema(Schema):
    """Lightweight workout summary embedded inside WorkoutExercise."""
    id = fields.Int(dump_only=True)
    date = fields.Date(dump_only=True)
    duration_minutes = fields.Int(dump_only=True)
    notes = fields.Str(dump_only=True)
 
 
class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(load_only=True)
    exercise_id = fields.Int(load_only=True)
    reps = fields.Int(load_default=None, allow_none=True)
    sets = fields.Int(load_default=None, allow_none=True)
    duration_seconds = fields.Int(load_default=None, allow_none=True)
 
    # Nested objects shown on dump
    exercise = fields.Nested(ExerciseSummarySchema, dump_only=True)
    workout = fields.Nested(WorkoutSummarySchema, dump_only=True)
 
    # Schema validations
    @validates("reps")
    def validate_reps(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Reps must be a positive integer.")
 
    @validates("sets")
    def validate_sets(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Sets must be a positive integer.")
 
    @validates("duration_seconds")
    def validate_duration_seconds(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Duration (seconds) must be a positive integer.")
 
 
# ── Exercise Schema ───────────────────────────────────────────────────────────
 
class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="Name cannot be blank."),
    )
    category = fields.Str(
        required=True,
        validate=validate.OneOf(
            VALID_CATEGORIES,
            error=f"Category must be one of: {', '.join(VALID_CATEGORIES)}.",
        ),
    )
    equipment_needed = fields.Bool(load_default=False)
 
    # Nested workouts shown when retrieving a single exercise
    workout_exercises = fields.List(
        fields.Nested(lambda: WorkoutExerciseWithWorkoutSchema()), dump_only=True
    )
 
 
class WorkoutExerciseWithWorkoutSchema(Schema):
    """WorkoutExercise entry with embedded workout — used inside ExerciseSchema."""
    id = fields.Int(dump_only=True)
    reps = fields.Int(dump_only=True, allow_none=True)
    sets = fields.Int(dump_only=True, allow_none=True)
    duration_seconds = fields.Int(dump_only=True, allow_none=True)
    workout = fields.Nested(WorkoutSummarySchema, dump_only=True)
 
 
# ── Workout Schema ────────────────────────────────────────────────────────────
 
class WorkoutExerciseWithExerciseSchema(Schema):
    """WorkoutExercise entry with embedded exercise — used inside WorkoutSchema."""
    id = fields.Int(dump_only=True)
    reps = fields.Int(dump_only=True, allow_none=True)
    sets = fields.Int(dump_only=True, allow_none=True)
    duration_seconds = fields.Int(dump_only=True, allow_none=True)
    exercise = fields.Nested(ExerciseSummarySchema, dump_only=True)
 
 
class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(
        required=True,
        error_messages={"required": "Date is required.", "null": "Date cannot be null."},
    )
    duration_minutes = fields.Int(
        required=True,
        validate=validate.Range(min=1, error="Duration must be at least 1 minute."),
    )
    notes = fields.Str(load_default=None, allow_none=True)
 
    # Nested exercises shown on GET /workouts/<id>
    workout_exercises = fields.List(
        fields.Nested(WorkoutExerciseWithExerciseSchema()), dump_only=True
    )
 
    # Schema validation: duration must be positive (mirrors model validation)
    @validates("duration_minutes")
    def validate_duration(self, value):
        if value <= 0:
            raise ValidationError("Duration must be a positive integer.")
 
 
# ── Instantiated schemas (reusable singletons) ────────────────────────────────
 
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True, exclude=["workout_exercises"])
 
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True, exclude=["workout_exercises"])
 
workout_exercise_schema = WorkoutExerciseSchema()
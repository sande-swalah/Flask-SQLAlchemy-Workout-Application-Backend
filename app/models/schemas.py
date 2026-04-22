from datetime import date

from marshmallow import Schema, fields, validates, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import Exercise, Workout, WorkoutExercise

class ExerciseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Exercise
        load_instance = False
        include_relationships = True

    # Schema Validations (2+)
    name = fields.Str(required=True, validate=lambda n: len(n) >= 3)
    category = fields.Str(required=True)

    @validates('name')
    def validate_name(self, name, **kwargs):
        if len(name.strip()) < 3:
            raise ValidationError("Exercise name must be at least 3 characters.")


class WorkoutExerciseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = WorkoutExercise
        load_instance = False
        include_fk = True

    exercise = fields.Nested('ExerciseSchema', only=('id', 'name', 'category'))


class WorkoutSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Workout
        load_instance = False
        include_relationships = True

    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, dump_only=True)

    # Schema Validations
    duration_minutes = fields.Int(required=True, validate=lambda d: 0 < d <= 1440)

    @validates('date')
    def validate_date(self, date_val, **kwargs):
        if date_val > date.today():
            raise ValidationError("Workout date cannot be in the future.")


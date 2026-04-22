from marshmallow import ValidationError

from app.models.schemas import ExerciseSchema, WorkoutExerciseSchema, WorkoutSchema


class RequestValidationError(Exception):
	def __init__(self, messages):
		super().__init__("Request payload validation failed")
		self.messages = messages


exercise_schema = ExerciseSchema()
workout_schema = WorkoutSchema()
workout_exercise_schema = WorkoutExerciseSchema()


def validate_exercise_payload(payload, partial=False):
	try:
		return exercise_schema.load(payload, partial=partial)
	except ValidationError as err:
		raise RequestValidationError(err.messages) from err


def validate_workout_payload(payload, partial=False):
	try:
		return workout_schema.load(payload, partial=partial)
	except ValidationError as err:
		raise RequestValidationError(err.messages) from err


def validate_workout_exercise_payload(payload):
	try:
		return workout_exercise_schema.load(payload)
	except ValidationError as err:
		raise RequestValidationError(err.messages) from err

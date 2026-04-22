from app.models.schemas import ExerciseSchema, WorkoutExerciseSchema, WorkoutSchema


_exercise_schema = ExerciseSchema()
_exercises_schema = ExerciseSchema(many=True)
_workout_schema = WorkoutSchema()
_workouts_schema = WorkoutSchema(many=True)
_workout_exercise_schema = WorkoutExerciseSchema()


def serialize_exercise(exercise):
    return _exercise_schema.dump(exercise)


def serialize_exercises(exercises):
    return _exercises_schema.dump(exercises)


def serialize_workout(workout):
    return _workout_schema.dump(workout)


def serialize_workouts(workouts):
    return _workouts_schema.dump(workouts)


def serialize_workout_exercise(workout_exercise):
    return _workout_exercise_schema.dump(workout_exercise)

from flask import abort, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException

from models import Exercise, Workout, WorkoutExercise, db
from schemas import (
    ExerciseSchema,
    WorkoutExerciseSchema,
    WorkoutSchema,
)

exercise_schema = ExerciseSchema()
exercise_list_schema = ExerciseSchema(many=True, exclude=["workout_exercises"])
exercise_detail_schema = ExerciseSchema()
workout_schema = WorkoutSchema()
workout_list_schema = WorkoutSchema(many=True, exclude=["workout_exercises"])
workout_detail_schema = WorkoutSchema()
workout_exercise_schema = WorkoutExerciseSchema()


def register_routes(app):

    @app.get("/")
    def index():
        return jsonify({"message": "Workout API is running."}), 200

    @app.get("/workouts")
    def list_workouts():
        workouts = Workout.query.order_by(Workout.date.desc(), Workout.id.desc()).all()
        return jsonify(workout_list_schema.dump(workouts)), 200

    @app.get("/workouts/<int:workout_id>")
    def get_workout(workout_id):
        workout = db.session.get(Workout, workout_id)
        if workout is None:
            abort(404, description="Workout not found.")
        return jsonify(workout_detail_schema.dump(workout)), 200

    @app.post("/workouts")
    def create_workout():
        payload = workout_schema.load(request.get_json() or {})
        workout = Workout(**payload)
        db.session.add(workout)
        commit_session()
        return jsonify(workout_detail_schema.dump(workout)), 201

    @app.delete("/workouts/<int:workout_id>")
    def delete_workout(workout_id):
        workout = db.session.get(Workout, workout_id)
        if workout is None:
            abort(404, description="Workout not found.")
        db.session.delete(workout)
        commit_session()
        return "", 204

    @app.get("/exercises")
    def list_exercises():
        exercises = Exercise.query.order_by(Exercise.name.asc()).all()
        return jsonify(exercise_list_schema.dump(exercises)), 200

    @app.get("/exercises/<int:exercise_id>")
    def get_exercise(exercise_id):
        exercise = db.session.get(Exercise, exercise_id)
        if exercise is None:
            abort(404, description="Exercise not found.")
        return jsonify(exercise_detail_schema.dump(exercise)), 200

    @app.post("/exercises")
    def create_exercise():
        payload = exercise_schema.load(request.get_json() or {})
        exercise = Exercise(**payload)
        db.session.add(exercise)
        commit_session()
        return jsonify(exercise_detail_schema.dump(exercise)), 201

    @app.delete("/exercises/<int:exercise_id>")
    def delete_exercise(exercise_id):
        exercise = db.session.get(Exercise, exercise_id)
        if exercise is None:
            abort(404, description="Exercise not found.")
        db.session.delete(exercise)
        commit_session()
        return "", 204

    

def commit_session():
    try:
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        raise ValidationError(
            {"database": ["Request violates a database constraint or uniqueness rule."]}
        ) from error
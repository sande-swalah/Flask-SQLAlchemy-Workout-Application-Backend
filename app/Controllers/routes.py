from flask import jsonify, request
from sqlalchemy.exc import IntegrityError

from app.models import db
from app.models.repository import Repository
from app.views.serializer import (
    serialize_exercise,
    serialize_exercises,
    serialize_workout,
    serialize_workout_exercise,
    serialize_workouts,
)
from app.views.validation import (
    RequestValidationError,
    validate_exercise_payload,
    validate_workout_exercise_payload,
    validate_workout_payload,
)

def register_routes(app):
    repo = Repository()

    @app.route('/exercises', methods=['GET'])
    def get_exercises():
        exercises = repo.list_exercises()
        return serialize_exercises(exercises), 200

    @app.route('/exercises/<int:id>', methods=['GET'])
    def get_exercise(id):
        exercise = repo.get_exercise_by_id(id)
        if not exercise:
            return jsonify({"error": "Exercise not found"}), 404
        return serialize_exercise(exercise), 200

    @app.route('/exercises', methods=['POST'])
    def create_exercise():
        try:
            data = validate_exercise_payload(request.get_json())
            exercise = repo.create_exercise(data)
            return serialize_exercise(exercise), 201
        except RequestValidationError as err:
            return jsonify({"errors": err.messages}), 400
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Exercise name must be unique"}), 400

    @app.route('/exercises/<int:id>', methods=['PUT', 'PATCH'])
    def update_exercise(id):
        exercise = repo.get_exercise_by_id(id)
        if not exercise:
            return jsonify({"error": "Exercise not found"}), 404

        try:
            data = validate_exercise_payload(request.get_json(), partial=True)
            updated = repo.update_exercise(exercise, data)
            return serialize_exercise(updated), 200
        except RequestValidationError as err:
            return jsonify({"errors": err.messages}), 400
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Exercise name must be unique"}), 400

    @app.route('/exercises/<int:id>', methods=['DELETE'])
    def delete_exercise(id):
        was_deleted = repo.delete_exercise(id)
        if not was_deleted:
            return jsonify({"error": "Exercise not found"}), 404
        return jsonify({"message": "Exercise deleted"}), 200

    @app.route('/workouts', methods=['GET'])
    def get_workouts():
        workouts = repo.list_workouts()
        return serialize_workouts(workouts), 200

    @app.route('/workouts/<int:id>', methods=['GET'])
    def get_workout(id):
        workout = repo.get_workout_by_id(id)
        if not workout:
            return jsonify({"error": "Workout not found"}), 404
        return serialize_workout(workout), 200

    @app.route('/workouts', methods=['POST'])
    def create_workout():
        try:
            data = validate_workout_payload(request.get_json())
            workout = repo.create_workout(data)
            return serialize_workout(workout), 201
        except RequestValidationError as err:
            return jsonify({"errors": err.messages}), 400

    @app.route('/workouts/<int:id>', methods=['PUT', 'PATCH'])
    def update_workout(id):
        workout = repo.get_workout_by_id(id)
        if not workout:
            return jsonify({"error": "Workout not found"}), 404

        try:
            data = validate_workout_payload(request.get_json(), partial=True)
            updated = repo.update_workout(workout, data)
            return serialize_workout(updated), 200
        except RequestValidationError as err:
            return jsonify({"errors": err.messages}), 400

    @app.route('/workouts/<int:id>', methods=['DELETE'])
    def delete_workout(id):
        was_deleted = repo.delete_workout(id)
        if not was_deleted:
            return jsonify({"error": "Workout not found"}), 404
        return jsonify({"message": "Workout deleted"}), 200

    @app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
    def add_exercise_to_workout(workout_id, exercise_id):
        workout = repo.get_workout_by_id(workout_id)
        exercise = repo.get_exercise_by_id(exercise_id)
        if not workout or not exercise:
            return jsonify({"error": "Workout or Exercise not found"}), 404

        data = request.get_json()
        try:
            we_data = validate_workout_exercise_payload(data)
            we = repo.create_workout_exercise(
                workout_id=workout_id,
                exercise_id=exercise_id,
                data=we_data,
            )
            return serialize_workout_exercise(we), 201
        except RequestValidationError as err:
            return jsonify({"errors": err.messages}), 400
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Exercise already added to this workout"}), 400





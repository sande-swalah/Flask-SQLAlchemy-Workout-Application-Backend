from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from app.models import Exercise, Workout, WorkoutExercise, db
from schemas import ExerciseSchema, WorkoutExerciseSchema, WorkoutSchema

def register_routes(app):
    exercise_schema = ExerciseSchema()
    exercises_schema = ExerciseSchema(many=True)
    workout_schema = WorkoutSchema()
    workouts_schema = WorkoutSchema(many=True)
    we_schema = WorkoutExerciseSchema()

    @app.route('/exercises', methods=['GET'])
    def get_exercises():
        exercises = Exercise.query.all()
        return exercises_schema.dump(exercises), 200

    @app.route('/exercises/<int:id>', methods=['GET'])
    def get_exercise(id):
        exercise = Exercise.query.get_or_404(id)
        return exercise_schema.dump(exercise), 200

    @app.route('/exercises', methods=['POST'])
    def create_exercise():
        try:
            data = exercise_schema.load(request.get_json())
            exercise = Exercise(**data)
            db.session.add(exercise)
            db.session.commit()
            return exercise_schema.dump(exercise), 201
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Exercise name must be unique"}), 400

    @app.route('/exercises/<int:id>', methods=['DELETE'])
    def delete_exercise(id):
        exercise = Exercise.query.get_or_404(id)
        db.session.delete(exercise)
        db.session.commit()
        return jsonify({"message": "Exercise deleted"}), 200

    @app.route('/workouts', methods=['GET'])
    def get_workouts():
        workouts = Workout.query.all()
        return workouts_schema.dump(workouts), 200

    @app.route('/workouts/<int:id>', methods=['GET'])
    def get_workout(id):
        workout = Workout.query.get_or_404(id)
        return workout_schema.dump(workout), 200

    @app.route('/workouts', methods=['POST'])
    def create_workout():
        try:
            data = workout_schema.load(request.get_json())
            workout = Workout(**data)
            db.session.add(workout)
            db.session.commit()
            return workout_schema.dump(workout), 201
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400

    @app.route('/workouts/<int:id>', methods=['DELETE'])
    def delete_workout(id):
        workout = Workout.query.get_or_404(id)
        db.session.delete(workout)
        db.session.commit()
        return jsonify({"message": "Workout deleted"}), 200

    @app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
    def add_exercise_to_workout(workout_id, exercise_id):
        Workout.query.get_or_404(workout_id)
        Exercise.query.get_or_404(exercise_id)

        data = request.get_json()
        try:
            we_data = we_schema.load(data)
            we = WorkoutExercise(
                workout_id=workout_id,
                exercise_id=exercise_id,
                reps=we_data.get('reps'),
                sets=we_data.get('sets'),
                duration_seconds=we_data.get('duration_seconds')
            )
            db.session.add(we)
            db.session.commit()
            return we_schema.dump(we), 201
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Exercise already added to this workout"}), 400





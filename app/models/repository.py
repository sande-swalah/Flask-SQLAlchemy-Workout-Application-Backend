#handling CRUD operations for our models
from models.domains import Exercise, Workout, WorkoutExercise
from models import db   

def commit_session():
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


def create_exercise(data):
    exercise = Exercise(**data)
    db.session.add(exercise)
    commit_session()
    return exercise 

def create_workout(data):
    workout = Workout(**data)
    db.session.add(workout)
    commit_session()
    return workout

def create_workout_exercise(data):
    workout_exercise = WorkoutExercise(**data)
    db.session.add(workout_exercise)
    commit_session()
    return workout_exercise

def get_exercise(exercise_id):
    return db.session.get(Exercise, exercise_id)

def get_workout(workout_id):
    return db.session.get(Workout, workout_id)

def delete_exercise(exercise_id):
    exercise = get_exercise(exercise_id)
    if exercise:
        db.session.delete(exercise)
        commit_session()
    
def delete_workout(workout_id):
    workout = get_workout(workout_id)
    if workout:
        db.session.delete(workout)
        commit_session()    


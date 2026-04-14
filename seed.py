#!/usr/bin/env python3
from app import app
from app.models import db, Exercise, Workout, WorkoutExercise
from datetime import date

with app.app_context():
    db.drop_all()
    db.create_all()

    # Exercises
    ex1 = Exercise(name="Bench Press", category="Chest", equipment_needed=True)
    ex2 = Exercise(name="Squats", category="Legs", equipment_needed=True)
    ex3 = Exercise(name="Plank", category="Core", equipment_needed=False)
    db.session.add_all([ex1, ex2, ex3])
    db.session.commit()

    # Workouts
    w1 = Workout(date=date(2026, 4, 10), duration_minutes=45, notes="Push day")
    w2 = Workout(date=date(2026, 4, 12), duration_minutes=60, notes="Leg day")
    db.session.add_all([w1, w2])
    db.session.commit()

    # WorkoutExercises
    we1 = WorkoutExercise(workout_id=w1.id, exercise_id=ex1.id, sets=4, reps=10)
    we2 = WorkoutExercise(workout_id=w1.id, exercise_id=ex3.id, duration_seconds=180)
    we3 = WorkoutExercise(workout_id=w2.id, exercise_id=ex2.id, sets=5, reps=8)
    db.session.add_all([we1, we2, we3])
    db.session.commit()

    print(" Database seeded")
#!/usr/bin/env python3

from datetime import date
from app import app
from models import db, Exercise, Workout, WorkoutExercise
 
 
with app.app_context():
    print("Clearing existing data...")
    # Delete in dependency order (join table first)
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()
 
    
    print("Seeding exercises...")
 
    squat       = Exercise(name="Barbell Back Squat",   category="strength",     equipment_needed=True)
    deadlift    = Exercise(name="Conventional Deadlift", category="strength",    equipment_needed=True)
    bench       = Exercise(name="Bench Press",           category="strength",    equipment_needed=True)
    pullup      = Exercise(name="Pull-Up",               category="strength",    equipment_needed=False)
    pushup      = Exercise(name="Push-Up",               category="strength",    equipment_needed=False)
    running     = Exercise(name="Treadmill Run",         category="cardio",      equipment_needed=True)
    rowing      = Exercise(name="Rowing Machine",        category="cardio",      equipment_needed=True)
    jump_rope   = Exercise(name="Jump Rope",             category="cardio",      equipment_needed=True)
    box_jump    = Exercise(name="Box Jump",              category="plyometrics", equipment_needed=True)
    burpee      = Exercise(name="Burpee",                category="plyometrics", equipment_needed=False)
    yoga_flow   = Exercise(name="Sun Salutation Flow",   category="flexibility", equipment_needed=False)
    hip_flexor  = Exercise(name="Hip Flexor Stretch",    category="flexibility", equipment_needed=False)
    plank       = Exercise(name="Plank Hold",            category="balance",     equipment_needed=False)
    single_leg  = Exercise(name="Single-Leg Deadlift",   category="balance",     equipment_needed=False)
 
    db.session.add_all([
        squat, deadlift, bench, pullup, pushup,
        running, rowing, jump_rope, box_jump, burpee,
        yoga_flow, hip_flexor, plank, single_leg,
    ])
    db.session.commit()
    print(f"  Created {Exercise.query.count()} exercises.")
 
    # ── Workouts ──────────────────────────────────────────────────────────────
    print("Seeding workouts...")
 
    w1 = Workout(
        date=date(2025, 4, 1),
        duration_minutes=60,
        notes="Heavy lower-body day. Focus on form."
    )
    w2 = Workout(
        date=date(2025, 4, 3),
        duration_minutes=45,
        notes="Upper-body push/pull superset."
    )
    w3 = Workout(
        date=date(2025, 4, 5),
        duration_minutes=30,
        notes="HIIT cardio circuit — no rest between rounds."
    )
    w4 = Workout(
        date=date(2025, 4, 7),
        duration_minutes=50,
        notes="Full-body strength with accessory work."
    )
    w5 = Workout(
        date=date(2025, 4, 9),
        duration_minutes=40,
        notes="Active recovery — mobility and core."
    )
 
    db.session.add_all([w1, w2, w3, w4, w5])
    db.session.commit()
    print(f"  Created {Workout.query.count()} workouts.")
 
    
    
    print("Seeding workout_exercises...")
 
    entries = [
        # Workout 1 — heavy lower body
        WorkoutExercise(workout=w1, exercise=squat,    sets=5, reps=5,  duration_seconds=None),
        WorkoutExercise(workout=w1, exercise=deadlift, sets=3, reps=5,  duration_seconds=None),
        WorkoutExercise(workout=w1, exercise=plank,    sets=3, reps=None, duration_seconds=60),
 
        # Workout 2 — upper body push/pull
        WorkoutExercise(workout=w2, exercise=bench,   sets=4, reps=8,  duration_seconds=None),
        WorkoutExercise(workout=w2, exercise=pullup,  sets=4, reps=8,  duration_seconds=None),
        WorkoutExercise(workout=w2, exercise=pushup,  sets=3, reps=15, duration_seconds=None),
 
        # Workout 3 — HIIT cardio
        WorkoutExercise(workout=w3, exercise=burpee,    sets=4, reps=15, duration_seconds=None),
        WorkoutExercise(workout=w3, exercise=box_jump,  sets=4, reps=10, duration_seconds=None),
        WorkoutExercise(workout=w3, exercise=jump_rope, sets=None, reps=None, duration_seconds=120),
 
        # Workout 4 — full body
        WorkoutExercise(workout=w4, exercise=squat,      sets=4, reps=8,  duration_seconds=None),
        WorkoutExercise(workout=w4, exercise=bench,      sets=4, reps=8,  duration_seconds=None),
        WorkoutExercise(workout=w4, exercise=rowing,     sets=None, reps=None, duration_seconds=600),
        WorkoutExercise(workout=w4, exercise=single_leg, sets=3, reps=10, duration_seconds=None),
 
        # Workout 5 — active recovery
        WorkoutExercise(workout=w5, exercise=yoga_flow,  sets=None, reps=None, duration_seconds=300),
        WorkoutExercise(workout=w5, exercise=hip_flexor, sets=None, reps=None, duration_seconds=120),
        WorkoutExercise(workout=w5, exercise=plank,      sets=3, reps=None,   duration_seconds=45),
        WorkoutExercise(workout=w5, exercise=running,    sets=None, reps=None, duration_seconds=1200),
    ]
 
    db.session.add_all(entries)
    db.session.commit()
    print(f"  Created {WorkoutExercise.query.count()} workout_exercise entries.")
 
    print("\nSeed complete!")
    print(f"  Exercises:         {Exercise.query.count()}")
    print(f"  Workouts:          {Workout.query.count()}")
    print(f"  WorkoutExercises:  {WorkoutExercise.query.count()}")
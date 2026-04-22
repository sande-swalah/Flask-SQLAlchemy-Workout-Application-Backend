from app.models import Exercise, Workout, WorkoutExercise, db



#CRUD OPERATIONS
class Repository:
    def list_exercises(self):
        return Exercise.query.all()

    def create_exercise(self, data):
        exercise = Exercise(
            name=data["name"],
            category=data["category"],
            equipment_needed=data.get("equipment_needed", False),
        )
        db.session.add(exercise)
        db.session.commit()
        return exercise

    def update_exercise(self, exercise, data):
        exercise.name = data.get("name", exercise.name)
        exercise.category = data.get("category", exercise.category)
        exercise.equipment_needed = data.get("equipment_needed", exercise.equipment_needed)
        db.session.commit()
        return exercise
    
    def create_workout(self, data):
        workout = Workout(
            date=data["date"],
            duration_minutes=data["duration_minutes"],
            notes=data.get("notes"),
        )
        db.session.add(workout)
        db.session.commit()
        return workout

    def list_workouts(self):
        return Workout.query.all()

    def update_workout(self, workout, data):
        workout.date = data.get("date", workout.date)
        workout.duration_minutes = data.get("duration_minutes", workout.duration_minutes)
        workout.notes = data.get("notes", workout.notes)
        db.session.commit()
        return workout
    
    def create_workout_exercise(self, workout_id, exercise_id, data):
        we = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=data.get("reps"),
            sets=data.get("sets"),
            duration_seconds=data.get("duration_seconds"),
        )
        db.session.add(we)
        db.session.commit()
        return we
    
    def get_exercise_by_id(self, exercise_id):
        return Exercise.query.get(exercise_id)
    
    def get_workout_by_id(self, workout_id):
        return Workout.query.get(workout_id)
    
    def delete_exercise(self, exercise_id):
        exercise = Exercise.query.get(exercise_id)
        if exercise:
            db.session.delete(exercise)
            db.session.commit()
            return True
        return False
    
    def delete_workout(self, workout_id):
        workout = Workout.query.get(workout_id)
        if workout:
            db.session.delete(workout)
            db.session.commit()
            return True
        return False
    
    



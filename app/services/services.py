

class Services:
    def __init__(self, workout_repository, exercise_repository, workout_exercise_repository):
        self.workout_repository = workout_repository
        self.exercise_repository = exercise_repository
        self.workout_exercise_repository = workout_exercise_repository
    
    def create_exercise(self, data):
        return self.exercise_repository.create_exercise(data)
    
    def create_workout(self, data):
        return self.workout_repository.create_workout(data)
    
    def create_workout_exercise(self, data):
        return self.workout_exercise_repository.create_workout_exercise(data)
    
    def get_exercise(self, exercise_id):
        return self.exercise_repository.get_exercise(exercise_id)
    
    def get_workout(self, workout_id):
        return self.workout_repository.get_workout(workout_id)
    
    def delete_exercise(self, exercise_id):
        self.exercise_repository.delete_exercise(exercise_id)
    
    def delete_workout(self, workout_id):
        self.workout_repository.delete_workout(workout_id)
    
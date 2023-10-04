import random
from student_data import student_data

def initialize_assignment(num_timeframes, num_activities):
    # Initialize a random assignment of activities to timeframes
    assignment = [[random.choice(range(num_activities))] for _ in range(num_timeframes)]
    return assignment

def evaluate_fitness(assignment, student_data):
    # Evaluate the fitness of the assignment based on student preferences and availability
    fitness = 0
    for timeframe, activity in enumerate(assignment):
        for student in student_data[timeframe][activity[0]]:
            fitness += 1  # Increase fitness for each student assigned to their preferred activity
    return fitness

def greedy_assignment(student_data, num_timeframes, num_activities):
    best_assignment = initialize_assignment(num_timeframes, num_activities)
    best_fitness = evaluate_fitness(best_assignment, student_data)

    # Number of iterations and improvement threshold (you can adjust these values)
    max_iterations = 1000
    improvement_threshold = 1

    for iteration in range(max_iterations):
        # Make a copy of the current best assignment
        current_assignment = best_assignment.copy()

        # Randomly select a timeframe and activity
        timeframe = random.randint(0, num_timeframes - 1)
        activity = random.randint(0, num_activities - 1)

        # Update the assignment for the selected timeframe
        current_assignment[timeframe] = [activity]

        # Evaluate the fitness of the new assignment
        current_fitness = evaluate_fitness(current_assignment, student_data)

        # Check if the new assignment is better
        if current_fitness > best_fitness:
            best_assignment = current_assignment
            best_fitness = current_fitness

            if best_fitness >= improvement_threshold:
                break

    return best_assignment

# Example usage:
num_timeframes = 21
num_activities = 6

# Mock student data (replace this with your actual data)
# student_data = [[[f"Student{i}" for i in range(6)] for _ in range(num_activities)] for _ in range(num_timeframes)]

def good(lst: list[list[int]]):
    mark = lst[0][0]
    counter = 1
    for [i] in lst[1:]:
        if i != mark:
            if counter < 2:
                return False
            counter = 1
            mark = i
        elif counter < 3:
            counter += 1
        else:
            return False
    return True

# print(good([[3], [5], [2], [1], [3], [0], [5], [0], [1], [0], [3], [3], [0], [1], [0], [4], [0], [3], [4], [5], [3]]))
# while not good((best_assignment := greedy_assignment(student_data, num_timeframes, num_activities))):
#     pass
# print(best_assignment)
# best_assignment = [[2], [1], [3], [3], [1], [2], [0], [4], [4], [0], [1], [4], [3], [0], [5], [3], [4], [0], [3], [3], [2]]
# best_assignment = [[0], [0], [0], [4], [4], [4], [5], [5], [1], [1], [5], [5], [3], [3], [3], [4], [4], [0], [0], [0], [4]]
# best_assignment = [[0], [0], [2], [2], [4], [4], [4], [1], [1], [5], [5], [2], [2], [3], [3], [4], [4], [0], [0], [3], [3]]
# best_assignment = [[3], [3], [1], [1], [4], [4], [4], [1], [1], [5], [5], [2], [2], [3], [3], [0], [0], [4], [4], [3], [3]]
# best_assignment = [[5], [5], [2], [2], [2], [3], [3], [1], [1], [3], [3], [5], [5], [3], [3], [0], [0], [0], [4], [4], [4]]
best_assignment = [[0], [2], [2], [3], [3], [3], [3], [1], [1], [5], [5], [5], [5], [3], [3], [0], [0], [0], [4], [4], [4]]
studs = set()
all_studs = set()
for [ass] in best_assignment:
    for time in student_data:
        studs.update(set(time[ass]))
        for acti in time:
            all_studs.update(set(acti))

# print(best_assignment)
print(len(studs), studs)
print(len(all_studs), all_studs)
print(studs.difference(all_studs))

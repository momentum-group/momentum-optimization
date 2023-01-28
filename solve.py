from pulp import *

def scheduling(people: list, max_hours: list, min_hours: list, preferred_hours: list, needed_capacity: list):
    """
    :param people: ???
    :param max_hours: maximum hours a given people[i] is allowed to work
    :param min_hours: minimum hours a given people[i] needs to work
    :param preferred_hours: ???
    :param needed_capacity: number of employees needed for each given time period
    """

    num_people = len(people)
    num_periods = len(people[0])

    prob = LpProblem("Work_Schedule_Optimization", LpMinimize)

    x = [[LpVariable(f"x_{i}_{j}", lowBound=0, upBound=1, cat='Binary') for j in range(num_periods)] for i in people]

    # Objective function
    # Minimize the maximum deviation from the preferred number of hours
    diffs = []
    for i in range(num_people):
        diff = LpVariable(f"diff_{i}")
        abs_diff = LpVariable(f"abs_diff_{i}", 0)
        diffs.append(abs_diff)
        prob += abs_diff >= diff
        prob += abs_diff >= -diff
        prob += sum([x[i][j] for j in range(num_periods)])/2 - preferred_hours[i] == diff
    prob += sum(diffs)

    # Constraints
    # Each person much work between their minimum and maximum number of hours
    for person in range(num_people):
        prob += sum(x[person])/2 <= max_hours[person]
        prob += sum(x[person])/2 >= min_hours[person]

    # Each period must have the correct number of people working
    for period in range(num_periods):
        prob += sum([x[person][period] for person in range(num_people)]) >= needed_capacity[period]

    # Each person can only work when they are available
    for person in range(num_people):
        for period in range(num_periods):
            if people[person][period] == 0:
                prob += x[person][period] == 0

    # Each person must work at least min_shift_length hours in a row
    # TODO

    # Solve
    prob.solve()
    print("Status:", LpStatus[prob.status])

    # Print solution
    for person in range(num_people):
        print("Person", person, ":", [value(x[person][period]) for period in range(num_periods)])

    # Print objective function value
    print("Objective function value:", value(prob.objective))

    return x

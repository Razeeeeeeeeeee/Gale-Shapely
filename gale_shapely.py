from datetime import datetime

class Employer:
    def __init__(self, name, skills_required, work_dates):
        self.name = name
        self.skills_required = skills_required
        self.work_dates = work_dates
        self.proposals = []

    def evaluate(self, employee):
        # Evaluate employee based on skills required and work dates
        if employee.skills == self.skills_required and employee.available_dates == self.work_dates:
            return 0
        elif employee.skills == self.skills_required:
            return 1
        elif employee.available_dates == self.work_dates:
            return 2
        else:
            return 3

    def propose_to(self, employee):
        # Employer proposes to employee
        self.proposals.append(employee)
        return employee.accept_proposal(self)

class Employee:
    def __init__(self, name, skills, available_dates):
        self.name = name
        self.skills = skills
        self.available_dates = available_dates
        self.matched_employer = None

    def accept_proposal(self, employer):
        # Employee accepts proposal if it's the best match
        if self.matched_employer is None:
            self.matched_employer = employer
            return True
        elif self.matched_employer.evaluate(self) > employer.evaluate(self):
            self.matched_employer = employer
            return True
        else:
            return False

def gale_shapley_matching(employers, employees):
    # Step 1: Initialization
    unmatched_employers = list(employers)
    matched_pairs = []

    # Step 2: Preference List Construction
    employer_preferences = {}
    for employer in employers:
        # Construct employer's preference list based on employee preferences
        employer_preferences[employer] = sorted(employees, key=lambda emp: employer.evaluate(emp))
    
    employee_preferences = {}
    for employee in employees:
        # Construct employee's preference list based on employer preferences
        employee_preferences[employee] = sorted(employers, key=lambda emp: employee.evaluate(emp))

    # Step 3: Matching Process
    while unmatched_employers:
        employer = unmatched_employers.pop(0)
        employee = employer_preferences[employer].pop(0)
        if employee in employer.propose_to(employee):  # Employer proposes to the employee
            matched_pairs.append((employer.name, employee.name))

    # Step 5: Output
    return matched_pairs

# Example usage
employers = [
    Employer("E1", "Full Stack", [datetime(2024, 5, 28), datetime(2024, 5, 29)]),
    Employer("E2", "Frontend", [datetime(2024, 5, 29), datetime(2024, 5, 30)]),
    Employer("E3", "Backend", [datetime(2024, 5, 30), datetime(2024, 5, 31)])
]

employees = [
    Employee("Emp1", "Full Stack", [datetime(2024, 5, 28), datetime(2024, 5, 29)]),
    Employee("Emp2", "Frontend", [datetime(2024, 5, 29), datetime(2024, 5, 30)]),
    Employee("Emp3", "Backend", [datetime(2024, 5, 30), datetime(2024, 5, 31)]),
    Employee("Emp4", "Full Stack", [datetime(2024, 5, 28), datetime(2024, 5, 29)]),
    Employee("Emp5", "Frontend", [datetime(2024, 5, 29), datetime(2024, 5, 30)])
]

matches = gale_shapley_matching(employers, employees)
print("Matched Pairs:")
for employer, employee in matches:
    print(f"{employer} matched with {employee}")

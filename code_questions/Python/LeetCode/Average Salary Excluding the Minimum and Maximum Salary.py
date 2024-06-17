class AverageSalary:

    def average(self, salary):
        """
        Average salary between minimum and maximum of all salaries
        """
        minSalary, maxSalary, totSalary = float('inf'), 0, 0

        for s in salary:
            totSalary += s
            if s < minSalary:
                minSalary = s
            if s > maxSalary:
                maxSalary = s
        
        return round((totSalary - minSalary - maxSalary) / (len(salary) - 2), 5)


if __name__ == "__main__":
    sol = AverageSalary()

    salaries = list(map(int, input().split()))

    print(sol.average(salaries))
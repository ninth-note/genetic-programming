import pandas as pd

def unpack_data(student_file, supervisor_file):

        # Load in the data for the two files
        students = pd.read_excel(student_file, header=None)
        supervisors = pd.read_excel(supervisor_file, header=None)

        # remove unnecessary items
        students = students.iloc[: , 1:]
        supervisors = supervisors.iloc[: , 1:]   

        # format as arrays
        students_array = students.to_numpy()
        supervisors_array = supervisors.to_numpy().flatten()

        # # Convert each row of the numpy array into a list of student preferences
        students_array = [list(students_array[i]) for i in range(students_array.shape[0])]

        return [students_array, supervisors_array]

def ranking_environment(input):

    student_file, supervisor_file = "Student-choices.xlsx", "Supervisors.xlsx"
    input = list(input.values())
    rank = ranking(student_file, supervisor_file, input)
    
    return rank

class ranking:

    def __init__(self, student_file, supervisor_file, input):
        self.columns = ["B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W"]
        data = unpack_data(student_file, supervisor_file)
        self.student_array = data[0]
        self.supervisor_array = data[1]
        self.input = input

    def find_column(self, assigned):

        # find corresponding column
        supervisor = (assigned - 1)
        column = self.columns[supervisor]

        return column

    def find_choice(self, assigned, student):

        choice = 0

        # find nth choice
        supervisor = (assigned - 1)
        choice = student[supervisor]

        return choice

    def test_capacity(self, more_info = False):

        caps = self.supervisor_array

        # simple test to see if any of the assigned lecturers had gone over capacity
        for assigned in self.input:
            
            caps[assigned - 1] -= 1

        if more_info: print("\nSupervisor capacities after assignment: %s\n" % str(caps))

        if (sum(caps) < 0):
            return False

        return True


    def examine(self, more_info = False):

        st = [1, 21]
        nd = [2, 22]
        rd = [3]

        columns = []
        choices = [None] * len(self.input)

        # first capacity test
        if self.test_capacity(more_info):
            print("\nCapacity Test ===> Passed\n")
        else:
            print("\nCapacity Test ===> Failed\n")
            return 0

        for student, assigned in enumerate(self.input):
        
            ranking = self.student_array[student]

            columns += self.find_column(assigned)
            choices[student] = self.find_choice(assigned, ranking)

        print("\nDetailed assignment:\n")

        for i in range(len(columns)):

            rank = ''

            if choices[i] in st:
                rank = str(choices[i]) + "st"
            elif choices[i] in nd:
                rank = str(choices[i]) + "nd"
            elif choices[i] in rd:
                rank = str(choices[i]) + "rd"
            else:
                rank = str(choices[i]) + "th"

            print("\tStudent '%d': Supervisor '%d' assigned, which is in Column '%s' ===> (%s choice)" % ((i + 1), self.input[i], columns[i], rank))


def main():
    
    data = {0: 15, 1: 21, 2: 21, 3: 10, 4: 20, 5: 4, 6: 8, 7: 8, 8: 7, 9: 16, 10: 10, 11: 11, 12: 21, 13: 13, 14: 22, 15: 15, 16: 4, 17: 22, 18: 13, 19: 5, 20: 14, 21: 20, 22: 12, 23: 10, 24: 9, 25: 17, 26: 15, 27: 18, 28: 3, 29: 7, 30: 3, 31: 6, 32: 21, 33: 20, 34: 14, 35: 6, 36: 10, 37: 20, 38: 4, 39: 1, 40: 2, 41: 22, 42: 1, 43: 19, 44: 17, 45: 1}

    rank = ranking_environment(data)

    rank.examine()


main()
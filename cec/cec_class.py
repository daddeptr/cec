class AgeError(Exception):
    def __repr__(self):
        return "AgeError exception: your child doesn't belong to this class"


class Class:
    def __init__(self, min_age, max_age, max_num_students, name, tuition):
        self.max_num_students = max_num_students
        self.name = name
        self.students = [] #deque([], maxlen=self.max_num_students)
        self.currently_enrolled_students = self._get_current_occupancy()
        self.tuition = tuition
        self.monthly_revenue = 0.
        if min_age < max_age:
            self.min_age = min_age
            self.max_age = max_age
        else:
            raise ValueError("min/max age not consistent: {},{}".fromat(min_age, max_age))

    def set_current_occupancy(self):
        self.currently_enrolled_students = len(self.students)

    def _get_current_occupancy(self):
        return len(self.students)

    def enroll_student(self, child):
        if self.currently_enrolled_students < self.max_num_students:
            if child.age_months >= self.min_age and child.age_months < self.max_age:
                self.students.append(child)
                self.currently_enrolled_students += 1
                self.monthly_revenue += child.tuition
            else:
                raise AgeError
        else:
            raise ValueError("Class '{}' is at capacity: {}".format(self.name, self.max_num_students))

    def adjust_tuition(self, pct, dollars=0):
        if dollars > 0:
            self.tuition = dollars
        else:
            if pct > 0:
                self.tuition *= 1. + pct / 100.
            else:
                raise ValueError("Tuition percentage: {}".format(self.tuition))

    def adjust_capacity(self, max_num):
        if isinstance(max_num, int):
            if max_num > 0:
                self.max_num_students = max_num
            else:
                raise ValueError("Negative capacity: {}".format(max_num))
        else:
            raise ValueError("Capacity must be an integer: {}".format(max_num))

    def enroll_students(self, students):
        while students:
            student = students.pop(0)
            student.set_tuition(self.tuition)
            try:
                self.enroll_student(student)
            except AgeError as e:
                print("{} - {} not enrolled".format(e, student))
                continue
            except ValueError as e:
                students.append(student)
                print("{} - {} students not enrolled".format(e, len(students)))
                break

        return students

    def graduate_students(self):
        old_students = []
        graduates = []
        for student in self.students:
            if student.age_months > self.max_age:
                graduates.append(student)
            else:
                old_students.append(student)
        self.students = old_students
        if graduates:
            self.set_current_occupancy()
        return graduates

    def __repr__(self):
        return "class '{}': from {} to {} months old - {} student(s) enrolled".format(self.name, self.min_age,
                                                                                      self.max_age,
                                                                                      self.currently_enrolled_students)
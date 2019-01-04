"""
It could serve as DB and a budget predictor app.
A DB would be useful/necessary, but to prototype, we could use CSV (probably easier to implement and get from current docs)

"""

#TODO: Implement drop due to TK; also make sure kids in the MB stays until September

class School:
    def __init__(self, name, classes, next_classes, months=0):
        self.name = name
        self.months = months
        self.month = self.months%12
        class_names = [_c.name.replace('-', '_').replace('.', '') for _c in classes]
        self.classes = class_names
        self.num_of_classes = len(classes)
        for i, _class in enumerate(classes):
            setattr(self, self.classes[i], _class)
        self._get_school_capacity()
        self.school_yearly_revenue_potential = self._get_revenue_potential(12)
        self.next_classes = next_classes
        self.waiting_list = {}
        self.history = []
        self.revenue = {}

    def __repr__(self):
        myself = "Welcome to {}!\nWe have {} class(es): {}\nThe school capacity is {} children, which may lead to ${}k annual revenue.".format(self.name, self.num_of_classes, self.classes, self.school_capacity, self.school_yearly_revenue_potential//1000)
        for c in self.classes:
            cls = getattr(self,c)
            myself = myself + "\n{}: {}".format(c,cls.currently_enrolled_students)
        myself = myself + "\nThis month we should make ${:.1f}k (vs {:.1f})".format(self.get_current_revenue()/1000, self._get_revenue_potential(1)/1000)
        myself = myself + "\nWaiting list: {}".format({k:len(v) for k,v in self.waiting_list.items()})
        return myself

    def _get_school_capacity(self):
        self.school_capacity = sum([c.max_num_students for c in [getattr(self, _c) for _c in self.classes]])

    def _get_revenue_potential(self, months):
        # months = 12
        return sum(
            [c.max_num_students * months * c.tuition for c in [getattr(self, _c) for _c in self.classes]])

    def get_current_revenue(self):
        return sum(
            [s.tuition for cls in [getattr(self, _c) for _c in self.classes] for s in cls.students])

    def increase_tuition(self, flat=None, per_class=None):
        print("Increasing tuition")
        if flat:
            for c in self.classes:
                cls = getattr(self, c)
                cls.adjust_tuition(flat)
        elif per_class:
            for c, p in per_class.items():
                cls = getattr(self, c)
                cls.adjust_tuition(p)
        self.school_yearly_revenue_potential = self._get_revenue_potential(12)

    def update_child_tuition(self):
        print("Updating child tuition")
        for c in self.classes:
            cls = getattr(self, c)
            for s in cls.students:
                s.tuition = cls.tuition

    def increase_class_size(self, per_class):
        for c, p in per_class.items():
            cls = getattr(self, c)
            cls.adjust_capacity(p)
        self._get_school_capacity()
        self._get_revenue_potential()

    def enroll_students(self, kids):
        waiting_list = {}
        for c, children in kids.items():
            cls = getattr(self,c)
            waiting = cls.enroll_students(children)
            if waiting:
                waiting_list[c] = waiting
        self.waiting_list = waiting_list


    def live_a_month(self):
        self.months += 1
        self.month = self.months % 12
        graduates = {}
        for c in self.classes:
            cls = getattr(self,c)
            for s in cls.students:
                s.grow(1)
            grads = cls.graduate_students()
            if grads:
                graduates[c] = grads
        if graduates:
            print(graduates)

        # Aging waiting list
        for _,lst in self.waiting_list.items():
            for s in lst:
                s.grow(1)

        return graduates

    def update_classes(self, graduates):
        for c in self.classes[::-1]:
            if c in graduates.keys():
                students = graduates[c]
            # for c,students in graduates.items():
                nc = self.next_classes[c]
                if nc:
                    cls = getattr(self,nc)
                    next_wave = cls.enroll_students(students)
                    if next_wave:
                        print("Some kids cannot move")
                        thcls = getattr(self,c)
                        _ = thcls.enroll_students(next_wave)
                        if _:
                            raise ValueError("We are losing kids")
                else:
                    print(c)
                    raise IndexError

        occupancy = []
        for c in self.classes:
            cls = getattr(self,c)
            occupancy.append(cls._get_current_occupancy())
        self.history.append(occupancy)
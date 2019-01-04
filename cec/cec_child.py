class Child:
    def __init__(self, age_months):
        self.age_months = age_months

    def set_tuition(self, tuition):
        self.tuition = tuition

    def grow(self, months):
        self.age_months += months

    def __repr__(self):
        return "I'm {} month(s) old.".format(self.age_months)
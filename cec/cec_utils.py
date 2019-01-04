from csv import DictReader
from .models import Student
import logging
logging.basicConfig(level=logging.DEBUG)

def load_to_db(filename):
    logging.debug(filename)
    student = Student(form.first_name.data, form.last_name.data, form.classroom.data,
                  form.date_of_birth.data, current_user.id)
    logging.debug(student)
    student.save()


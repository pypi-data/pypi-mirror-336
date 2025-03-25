class Course: 

    def __init__(self, name, duration, link):
        self.name = name
        self.duration = duration
        self.link = link

    def __repr__(self):
        return f"{self.name} [{self.duration} hrs] ({self.link})"

courses = [
    Course("Introducción a Linux", 15, "Primer URL"),
    Course("Personalización a Linux", 3, "Segunda URL"),
    Course("Introducción al Hacking", 53, "Tercer URL")
]

def list_courses():
    for course in courses:
        print(course)

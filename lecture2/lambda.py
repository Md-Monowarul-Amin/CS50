people = [
    {"name":"Harry", "house": "Gryffindor"},
    {"name":"cho", "house":"Ravenclas"},
    {"name":"Dracco", "house":"Slytherin"},
]


def f(people):
    return people["name"]

people.sort(key=lambda person: person["name"])
print(people)

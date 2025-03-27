from random import randint

# Create an array of object data
body_data = []

# throwing balls
for i in range(10):
    body_data.append({
        'type': 'sphere',
        'pos': (0, i * 2, 0),
        'scale': (1, 1, 1),
        'color': (i / 10, 0, 1 - i / 10),
        'mass': 1,
        'vec': (i, 0, i)
    })

# Create target object data
for i in range(10):
    body_data.append({
        'type': 'box',
        'pos': (20, i * 2, 0),
        'scale': (0.5, 1, 2),
        'color': (i / 10, 0, 1 - i / 10),
        'mass': 1
    })
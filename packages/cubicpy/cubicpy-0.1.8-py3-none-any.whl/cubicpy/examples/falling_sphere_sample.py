from random import randint

# Create an array of object data
body_data = []

# Stack 10 levels of cubees

body_data.append({
    'type': 'sphere',
    'pos': (0, 0, randint(5, 20)),  # Position: x, y, z
    'scale': (1, 1, 1),  # Size: width, depth, height
    'color': (1, 0, 0),  # Color: red, green, blue (0-1)
    'mass': 1  # Mass (optional)
})
# Create an array of object data
body_data = []

# Stack 10 levels of cubees
for i in range(10):
    body_data.append({
        'type': 'sphere',
        'pos': (0, 0, i),  # Position: x, y, z
        'scale': (1, 1, 1),  # Size: width, depth, height
        'color': (i/10, 0, 1-i/10),  # Color: red, green, blue (0-1)
        'mass': 1  # Mass (optional)
    })
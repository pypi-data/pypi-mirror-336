body_data = []
for i in range(10):
    body_data.append({
        'type': 'cylinder',
        'pos': (0, 0, i),
        'scale': (1, 1, 1),
        'color': (i / 10, 0, 1 - i / 10),
    })
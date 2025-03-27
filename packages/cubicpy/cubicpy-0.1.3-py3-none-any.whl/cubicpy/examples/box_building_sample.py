body_data = []

for l in range(10):
    for k in range(2):
        body_data.append({
            'type': 'box',
            'pos': (0, k * 9.5, 10 + l * 11),
            'scale': (10, 0.5, 1),
            'color': (1, 0, 0),
        })
        body_data.append({
            'type': 'box',
            'pos': (k * 9, 0.5, 10 + l * 11),
            'scale': (1, 9, 1),
            'color': (1, 0, 0),
        })

        for j in range(2):
            for i in range(10):
                body_data.append({
                    'type': 'box',
                    'pos': (k * 9, j * 9, i + l * 11),
                    'scale': (1, 1, 1),
                    'color': (i / 10, 0, 1 - i / 10),
                })
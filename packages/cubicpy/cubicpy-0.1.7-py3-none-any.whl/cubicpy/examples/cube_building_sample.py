body_data = []

# ユニットを積み上げる（10段）
for l in range(10):
    # 柱の配置（X方向）
    for k in range(2):
        body_data.append({
            'type': 'cube',
            'pos': (0, k * 9.5, 10 + l * 11),
            'scale': (10, 0.5, 1),
            'color': (1, 0, 0),
        })
        body_data.append({
            'type': 'cube',
            'pos': (k * 9, 0.5, 10 + l * 11),
            'scale': (1, 9, 1),
            'color': (1, 0, 0),
        })

        # 柱の配置（Y方向）
        for j in range(2):
            # 柱の作成（10段）
            for i in range(10):
                body_data.append({
                    'type': 'cube',
                    'pos': (k * 9, j * 9, i + l * 11),
                    'scale': (1, 1, 1),
                    'color': (i / 10, 0, 1 - i / 10),
                })
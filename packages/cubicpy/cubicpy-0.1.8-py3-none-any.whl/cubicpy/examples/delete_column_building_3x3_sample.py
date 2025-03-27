body_data = []
step_num = 10

# Z軸
for k in range(step_num):
    # Y軸
    for j in range(3):
        # X軸
        for i in range(3):
            if j < 2:
                # Y方向の梁
                pos_y_beam = (i * 9.25, 0.5 + 9.25 * j, 9 + k * 10)
                scale_y_beam = (0.5, 8.75, 1)
                body_data.append({
                    'type': 'cube',
                    'pos': pos_y_beam,
                    'scale': scale_y_beam,
                    'color': (1, 0, 0),
                    'mass': 1
                })

            if i < 2:
                # X方向の梁
                pos_x_beam = (i * 9.5, j * 9.25, 9 + k * 10)
                scale_x_beam = (9.5, 0.5, 1)
                body_data.append({
                    'type': 'cube',
                    'pos': pos_x_beam,
                    'scale': scale_x_beam,
                    'color': (1, 0, 0),
                    'mass': 1
                })

            # 柱の作成
            pos_pillar = (i * 9, j * 9, k * 10)
            scale_pillar = (1, 1, 9)
            body_data.append({
                'type': 'cube',
                'pos': pos_pillar,
                'scale': scale_pillar,
                'color': (i, j, k),
                'mass': 1,
                'remove': True if i < 2 and j < 2 and k == 0 else False
            })

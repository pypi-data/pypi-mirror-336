body_data = []
step_num = 10

# Z軸
for k in range(step_num):
    # Y軸
    for j in range(2):
        # X軸
        for i in range(2):
            if j < 1:
                # Y方向の梁
                pos_y_beam = (i * 9.5, 0.5, 9 + k * 10)
                scale_y_beam = (0.5, 9, 1)
                body_data.append({
                    'type': 'cube',
                    'pos': pos_y_beam,
                    'scale': scale_y_beam,
                    'color': (1, 0, 0),
                    'mass': 1
                })

            if i < 1:
                # X方向の梁
                pos_x_beam = (0, j * 9.5, 9 + k * 10)
                scale_x_beam = (10, 0.5, 1)
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
                'remove': True if i < 2 and j == 0 and k == 0 else False
            })

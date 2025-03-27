# api_method.py の修正

class ApiMethod:
    """オブジェクト作成と操作のためのAPIメソッド"""

    def __init__(self, app):
        self.app = app
        self.object_data = []  # リセット用にオブジェクトデータを保存

    def add_box(self, position=(0, 0, 0), scale=(1, 1, 1), color=(0.5, 0.5, 0.5), mass=1, color_alpha=1, hpr=(0, 0, 0), base_point=0, remove=False):
        """箱を追加"""
        box_data = {
            'type': 'box',
            'pos': position,
            'scale': scale,
            'color': color,
            'mass': mass,
            'color_alpha': color_alpha,
            'hpr': hpr,
            'base_point': base_point,
            'remove': remove
        }
        self.object_data.append(box_data)
        return box_data

    def add_sphere(self, position=(0, 0, 0), scale=(1, 1, 1), color=(0.5, 0.5, 0.5), mass=1, color_alpha=1, hpr=(0, 0, 0), base_point=0, remove=False):
        """球を追加"""
        sphere_data = {
            'type': 'sphere',
            'pos': position,
            'scale': scale,
            'color': color,
            'mass': mass,
            'color_alpha': color_alpha,
            'hpr': hpr,
            'base_point': base_point,
            'remove': remove
        }
        self.object_data.append(sphere_data)
        return sphere_data

    def add_cylinder(self, position=(0, 0, 0), scale=(1, 1, 1), color=(0.5, 0.5, 0.5), mass=1, color_alpha=1, hpr=(0, 0, 0), base_point=0, remove=False):
        """円柱を追加"""
        cylinder_data = {
            'type': 'cylinder',
            'pos': position,
            'scale': scale,
            'color': color,
            'mass': mass,
            'color_alpha': color_alpha,
            'hpr': hpr,
            'base_point': base_point,
            'remove': remove
        }
        self.object_data.append(cylinder_data)
        return cylinder_data

    def add_ground(self, color=(0, 1, 0), color_alpha=0.3):
        """平面の地面を追加"""
        ground_data = {
            'type': 'box',
            'pos': (-500, -500, -1),
            'scale': (1000, 1000, 1),
            'color': color,
            'mass': 0,
            'color_alpha': color_alpha
        }
        self.object_data.append(ground_data)
        return ground_data

    def add(self, obj_type, **kwargs):
        """汎用オブジェクト追加メソッド"""
        position = kwargs.get('position', kwargs.get('pos', (0, 0, 0)))
        scale = kwargs.get('scale', (1, 1, 1))
        color = kwargs.get('color', (0.5, 0.5, 0.5))
        mass = kwargs.get('mass', 1)
        color_alpha = kwargs.get('color_alpha', 1)
        hpr = kwargs.get('hpr', (0, 0, 0))
        base_point = kwargs.get('base_point', 0)
        remove = kwargs.get('remove', False)
        if obj_type == 'box':
            self.add_box(position, scale, color, mass, color_alpha, hpr, base_point, remove)
        elif obj_type == 'sphere':
            self.add_sphere(position, scale, color, mass, color_alpha, hpr, base_point, remove)
        elif obj_type == 'cylinder':
            self.add_cylinder(position, scale, color, mass, color_alpha, hpr, base_point, remove)

        else:
            raise ValueError(f"未知のオブジェクトタイプ: {obj_type}")

    def from_body_data(self, body_data):
        """body_dataリストからオブジェクトを作成"""
        for data in body_data:
            data_copy = data.copy()  # 元のデータを変更しないようにコピー
            obj_type = data_copy.pop('type', 'box')
            self.add(obj_type, **data_copy)
        return self

    def clear_data(self):
        """保存したオブジェクトデータをクリア"""
        self.object_data = []

    def get_object_data(self):
        """保存したオブジェクトデータのコピーを取得"""
        return self.object_data.copy()
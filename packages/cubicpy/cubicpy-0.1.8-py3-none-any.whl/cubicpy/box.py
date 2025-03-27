from panda3d.core import Vec3
from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape
from . import get_position_offset


class Box:
    def __init__(self, app, box):
        # print(box)
        self.app = app

        # スケール・色・質量の設定
        self.node_scale = Vec3(box['scale']) if 'scale' in box else (1, 1, 1)
        self.node_color = box['color'] if 'color' in box else (0.5, 0.5, 0.5)
        self.node_mass = box['mass'] if 'mass' in box else 1
        self.node_hpr = box['hpr'] if 'hpr' in box else Vec3(0, 0, 0)
        self.color_alpha = box['color_alpha'] if 'color_alpha' in box else 1
        # 配置するときの位置基準 (0: 原点に近い角が基準, 1: 底面の中心が基準, 2: 立方体の重心が基準)
        self.base_point = box['base_point'] if 'base_point' in box else 0
        self.remove_selected = box['remove'] if 'remove' in box else False

        # 配置位置の計算
        self.node_pos = Vec3(box['pos']) + get_position_offset(self)

        # 物理形状（スケールを適用）
        if box['scale'] in self.app.model_manager.box_shapes:
            self.box_shape = self.app.model_manager.box_shapes[box['scale']]
        else:
            self.box_shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
            self.app.model_manager.box_shapes[box['scale']] = self.box_shape

        # Bullet剛体ノード
        self.rigid_box = BulletRigidBodyNode('Box')
        self.rigid_box.setMass(self.node_mass)
        self.rigid_box.addShape(self.box_shape)
        self.rigid_box.setRestitution(self.app.RESTITUTION)
        self.rigid_box.setFriction(self.app.FRICTION)
        self.app.physics.bullet_world.attachRigidBody(self.rigid_box)

        # ノードパス
        self.box_node = self.app.world_node.attachNewNode(self.rigid_box)
        self.box_node.setPos(self.node_pos)
        self.box_node.setScale(self.node_scale)
        self.box_node.setColor(*self.node_color, self.color_alpha)
        self.box_node.setHpr(self.node_hpr)
        self.app.model_manager.box_model.copyTo(self.box_node)

        if self.color_alpha < 1:
            self.box_node.setTransparency(1)  # 半透明を有効化

    def update(self):
        """ 物理エンジンの位置を更新 """
        self.box_node.setPos(self.box_node.node().getPos())

    def remove(self):
        """ ボックスを削除 """
        self.app.physics.bullet_world.removeRigidBody(self.box_node.node())
        self.box_node.removeNode()
        del self.box_node
        del self.box_shape  # 削除処理

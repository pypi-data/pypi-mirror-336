from panda3d.core import Vec3
from panda3d.bullet import BulletRigidBodyNode, BulletCylinderShape
from . import get_position_offset


class Cylinder:
    def __init__(self, app, cylinder):
        # print(cylinder)
        self.app = app

        # スケール・色・質量の設定
        self.node_scale = Vec3(cylinder['scale']) if 'scale' in cylinder else (1, 1, 1)
        self.node_color = cylinder['color'] if 'color' in cylinder else (0.5, 0.5, 0.5)
        self.node_mass = cylinder['mass'] if 'mass' in cylinder else 1
        self.node_hpr = cylinder['hpr'] if 'hpr' in cylinder else Vec3(0, 0, 0)
        self.color_alpha = cylinder['color_alpha'] if 'color_alpha' in cylinder else 1
        # 配置するときの位置基準 (0: 原点に近い角が基準, 1: 底面の中心が基準, 2: 立方体の重心が基準)
        self.base_point = cylinder['base_point'] if 'base_point' in cylinder else 0
        self.remove_selected = cylinder['remove'] if 'remove' in cylinder else False
        # 初速度ベクトルの設定を追加
        self.vec = Vec3(cylinder['vec']) if 'vec' in cylinder else Vec3(0, 0, 0)

        # 配置位置の計算
        self.node_pos = Vec3(cylinder['pos']) + get_position_offset(self)

        # 物理形状（スケールを適用）
        if cylinder['scale'] in self.app.model_manager.cylinder_shapes:
            self.cylinder_shape = self.app.model_manager.cylinder_shapes[cylinder['scale']]
        else:
            self.cylinder_shape = BulletCylinderShape(0.5, 1)
            self.app.model_manager.cylinder_shapes[cylinder['scale']] = self.cylinder_shape

        # Bullet剛体ノード
        self.rigid_cylinder = BulletRigidBodyNode('Cylinder')
        self.rigid_cylinder.setMass(self.node_mass)
        self.rigid_cylinder.addShape(self.cylinder_shape)
        self.rigid_cylinder.setRestitution(self.app.RESTITUTION)
        self.rigid_cylinder.setFriction(self.app.FRICTION)
        self.app.physics.bullet_world.attachRigidBody(self.rigid_cylinder)

        # ノードパス
        self.cylinder_node = self.app.world_node.attachNewNode(self.rigid_cylinder)
        self.cylinder_node.setPos(self.node_pos)
        self.cylinder_node.setScale(self.node_scale)
        self.cylinder_node.setColor(*self.node_color, self.color_alpha)
        self.cylinder_node.setHpr(self.node_hpr)
        self.app.model_manager.cylinder_model.copyTo(self.cylinder_node)

        if self.color_alpha < 1:
            self.cylinder_node.setTransparency(1)  # 半透明を有効化

    def update(self):
        """ 物理エンジンの位置を更新 """
        self.cylinder_node.setPos(self.cylinder_node.node().getPos())

    def remove(self):
        """ ボックスを削除 """
        self.app.physics.bullet_world.removeRigidBody(self.cylinder_node.node())
        self.cylinder_node.removeNode()
        del self.cylinder_node
        del self.cylinder_shape  # 削除処理

    def apply_velocity(self):
        """オブジェクトに初速を与える"""
        if self.vec != Vec3(0, 0, 0):
            self.cylinder_node.node().setLinearVelocity(self.vec)

from panda3d.core import Vec3
from panda3d.bullet import BulletRigidBodyNode, BulletCylinderShape


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
        # 位置基準（corner_near_origin, bottom_center, gravity_center or None）
        self.position_mode = cylinder['position_mode'] if 'position_mode' in cylinder else None

        # 配置位置の計算
        self.node_pos = Vec3(cylinder['pos']) + self.get_position_offset()

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

    def get_position_offset(self):
        """ `position_mode` に基づいてオフセットを返す """
        half_scale = self.node_scale / 2
        if self.position_mode == 'corner_near_origin':
            return half_scale  # 原点側の角
        elif self.position_mode == 'bottom_center':
            return Vec3(0, 0, half_scale.z)  # 底面の中心
        elif self.position_mode == 'gravity_center':
            return Vec3(0, 0, 0)  # 重心
        return half_scale  # デフォルト（原点側の角）

    def update(self):
        """ 物理エンジンの位置を更新 """
        self.cylinder_node.setPos(self.cylinder_node.node().getPos())

    def remove(self):
        """ ボックスを削除 """
        self.app.physics.bullet_world.removeRigidBody(self.cylinder_node.node())
        self.cylinder_node.removeNode()
        del self.cylinder_node
        del self.cylinder_shape  # 削除処理

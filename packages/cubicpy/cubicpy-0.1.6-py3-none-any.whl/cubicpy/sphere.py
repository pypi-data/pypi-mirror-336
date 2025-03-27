from panda3d.core import Vec3
from panda3d.bullet import BulletRigidBodyNode, BulletSphereShape
from . import get_position_offset


class Sphere:
    def __init__(self, app, sphere):
        # print(sphere)
        self.app = app

        # スケール・色・質量の設定
        self.node_scale = Vec3(sphere['scale']) if 'scale' in sphere else (1, 1, 1)
        self.node_color = sphere['color'] if 'color' in sphere else (0.5, 0.5, 0.5)
        self.node_mass = sphere['mass'] if 'mass' in sphere else 1
        self.node_hpr = sphere['hpr'] if 'hpr' in sphere else Vec3(0, 0, 0)
        self.color_alpha = sphere['color_alpha'] if 'color_alpha' in sphere else 1
        # 配置するときの位置基準 (0: 原点に近い角が基準, 1: 底面の中心が基準, 2: 立方体の重心が基準)
        self.base_point = sphere['base_point'] if 'base_point' in sphere else 0
        self.remove_selected = sphere['remove'] if 'remove' in sphere else False

        # 配置位置の計算
        self.node_pos = Vec3(sphere['pos']) + get_position_offset(self)

        # 物理形状（スケールを適用）
        if sphere['scale'] in self.app.model_manager.sphere_shapes:
            self.sphere_shape = self.app.model_manager.sphere_shapes[sphere['scale']]
        else:
            self.sphere_shape = BulletSphereShape(0.5)
            self.app.model_manager.sphere_shapes[sphere['scale']] = self.sphere_shape

        # Bullet剛体ノード
        self.rigid_sphere = BulletRigidBodyNode('Sphere')
        self.rigid_sphere.setMass(self.node_mass)
        self.rigid_sphere.addShape(self.sphere_shape)
        self.rigid_sphere.setRestitution(self.app.RESTITUTION)
        self.rigid_sphere.setFriction(self.app.FRICTION)
        self.app.physics.bullet_world.attachRigidBody(self.rigid_sphere)

        # ノードパス
        self.sphere_node = self.app.world_node.attachNewNode(self.rigid_sphere)
        self.sphere_node.setPos(self.node_pos)
        self.sphere_node.setScale(self.node_scale)
        self.sphere_node.setColor(*self.node_color, self.color_alpha)
        self.sphere_node.setHpr(self.node_hpr)
        self.app.model_manager.sphere_model.copyTo(self.sphere_node)

        if self.color_alpha < 1:
            self.sphere_node.setTransparency(1)  # 半透明を有効化

    def update(self):
        """ 物理エンジンの位置を更新 """
        self.sphere_node.setPos(self.sphere_node.node().getPos())

    def remove(self):
        """ ボックスを削除 """
        self.app.physics.bullet_world.removeRigidBody(self.sphere_node.node())
        self.sphere_node.removeNode()
        del self.sphere_node
        del self.sphere_shape  # 削除処理

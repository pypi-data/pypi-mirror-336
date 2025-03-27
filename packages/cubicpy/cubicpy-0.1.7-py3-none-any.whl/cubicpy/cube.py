from panda3d.core import Vec3
from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape
from . import get_position_offset


class Cube:
    def __init__(self, app, cube):
        # print(cube)
        self.app = app

        # スケール・色・質量の設定
        self.node_scale = Vec3(cube['scale']) if 'scale' in cube else (1, 1, 1)
        self.node_color = cube['color'] if 'color' in cube else (0.5, 0.5, 0.5)
        self.node_mass = cube['mass'] if 'mass' in cube else 1
        self.node_hpr = cube['hpr'] if 'hpr' in cube else Vec3(0, 0, 0)
        self.color_alpha = cube['color_alpha'] if 'color_alpha' in cube else 1
        # 配置するときの位置基準 (0: 原点に近い角が基準, 1: 底面の中心が基準, 2: 立方体の重心が基準)
        self.base_point = cube['base_point'] if 'base_point' in cube else 0
        self.remove_selected = cube['remove'] if 'remove' in cube else False
        # 初速度ベクトルの設定を追加
        self.vec = Vec3(cube['vec']) if 'vec' in cube else Vec3(0, 0, 0)

        # 配置位置の計算
        self.node_pos = Vec3(cube['pos']) + get_position_offset(self)

        # 物理形状（スケールを適用）
        if cube['scale'] in self.app.model_manager.cube_shapes:
            self.cube_shape = self.app.model_manager.cube_shapes[cube['scale']]
        else:
            self.cube_shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
            self.app.model_manager.cube_shapes[cube['scale']] = self.cube_shape

        # Bullet剛体ノード
        self.rigid_cube = BulletRigidBodyNode('Cube')
        self.rigid_cube.setMass(self.node_mass)
        self.rigid_cube.addShape(self.cube_shape)
        self.rigid_cube.setRestitution(self.app.RESTITUTION)
        self.rigid_cube.setFriction(self.app.FRICTION)
        self.app.physics.bullet_world.attachRigidBody(self.rigid_cube)

        # ノードパス
        self.cube_node = self.app.world_node.attachNewNode(self.rigid_cube)
        self.cube_node.setPos(self.node_pos)
        self.cube_node.setScale(self.node_scale)
        self.cube_node.setColor(*self.node_color, self.color_alpha)
        self.cube_node.setHpr(self.node_hpr)
        self.app.model_manager.cube_model.copyTo(self.cube_node)

        if self.color_alpha < 1:
            self.cube_node.setTransparency(1)  # 半透明を有効化

    def update(self):
        """ 物理エンジンの位置を更新 """
        self.cube_node.setPos(self.cube_node.node().getPos())

    def remove(self):
        """ ボックスを削除 """
        self.app.physics.bullet_world.removeRigidBody(self.cube_node.node())
        self.cube_node.removeNode()
        del self.cube_node
        del self.cube_shape  # 削除処理

    def apply_velocity(self):
        """オブジェクトに初速を与える"""
        if self.vec != Vec3(0, 0, 0):
            self.cube_node.node().setLinearVelocity(self.vec)

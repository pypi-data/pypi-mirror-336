from panda3d.core import Vec3
from panda3d.bullet import BulletRigidBodyNode


class Cone:
    def __init__(self, base, cone):
        self.base = base

        node_scale = cone['scale']
        node_center = node_scale / 2
        node_pos = cone['pos'] + Vec3(0.5, 0.5, 0.54)
        node_color = cone['color']
        node_mass = node_scale[0] * node_scale[1] * node_scale[2]

        rigid_cone = BulletRigidBodyNode('Cone')
        rigid_cone.setMass(node_mass)
        rigid_cone.addShape(self.base.cone_shape)
        self.base.bullet_world.attachRigidBody(rigid_cone)

        self.cone_node = self.base.render.attachNewNode(rigid_cone)
        self.cone_node.setPos(node_pos)
        self.cone_node.setScale(node_scale)
        self.cone_node.setColor(*node_color, 1)
        self.base.cone_model.copyTo(self.cone_node)

    # Update
    def update(self):
        pass

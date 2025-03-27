from enum import Enum
from panda3d.core import Vec3

class BasePoint(Enum):
    CORNER_NEAR_ORIGIN = 0
    BOTTOM_CENTER = 1
    GRAVITY_CENTER = 2

# そして関数は以下のように変更：
def get_position_offset(self):
    """ `base_point` に基づいてオフセットを返す """
    half_scale = self.node_scale / 2
    if self.base_point == BasePoint.CORNER_NEAR_ORIGIN:
        return half_scale  # 原点側の角
    elif self.base_point == BasePoint.BOTTOM_CENTER:
        return Vec3(0, 0, half_scale.z)  # 底面の中心
    elif self.base_point == BasePoint.GRAVITY_CENTER:
        return Vec3(0, 0, 0)  # 重心
    return half_scale  # デフォルト（原点側の角）
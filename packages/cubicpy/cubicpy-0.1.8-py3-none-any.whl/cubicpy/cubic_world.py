import sys
from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import *
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletDebugNode
from .camera import CameraControl
from .box import Box
from .sphere import Sphere
from .cylinder import Cylinder
from .axis import Axis


class CubicWorld(ShowBase):
    GRAVITY_VECTOR = Vec3(0, 0, -9.81)
    RESTITUTION = 0  # 反発係数
    FRICTION = 0.5  # 摩擦係数

    def __init__(self, window_title="CubicPy World", window_size=(1800, 1200), gravity_factor=-6):
        """
        CubicWorldを初期化

        Parameters:
        -----------
        window_title : str
            ウィンドウのタイトル
        window_size : tuple
            ウィンドウサイズ (幅, 高さ)
        gravity_factor : int
            重力の強さ（負の値＝重力が下向き）
        """
        # ShowBaseを初期化（Panda3Dの基本機能）
        ShowBase.__init__(self)
        self.gravity_factor = gravity_factor
        self.gravity_vector = self.GRAVITY_VECTOR * 10 ** gravity_factor
        self.box_shapes = {}
        self.sphere_shapes = {}
        self.cylinder_shapes = {}
        self.body_objects = []
        self.tilt_x = 0
        self.tilt_y = 0
        self.tilt_speed = 5
        self.target_tilt_x = 0
        self.target_tilt_y = 0
        self.tilt_step = 0  # 現在のフレーム数
        self.max_tilt_frames = 10  # 10フレームかけて傾ける

        # ウィンドウ設定
        self.setup_window(window_title, window_size)

        # 世界の基本要素を設定
        self.setup_world(gravity_factor)

        # オブジェクトリスト
        self.objects = []

        # キー操作の設定
        self.setup_controls()

    def setup_window(self, title, size):
        """ウィンドウの設定"""
        props = WindowProperties()
        props.setTitle(title)
        props.setSize(*size)
        self.win.requestProperties(props)

    def setup_world(self, gravity_factor):
        """世界の基本設定"""
        # 重力設定
        self.gravity_vector = Vec3(0, 0, -9.81) * (10 ** gravity_factor)

        # 物理エンジン
        self.bullet_world = BulletWorld()
        self.bullet_world.setGravity(self.gravity_vector)

        # デバッグ表示
        self.setup_debug()

        # 世界のノード
        self.world_node = self.render.attachNewNode("world_node")

        # 基本要素の追加
        self.camera_control = CameraControl(self)
        self.axis = Axis(self)

        # 物理アップデートタスク
        self.taskMgr.add(self.update_physics, "update_physics")

    def setup_debug(self):
        """デバッグ表示の設定"""
        self.debug_node = BulletDebugNode("debug")
        self.debug_np = self.render.attachNewNode(self.debug_node)
        self.bullet_world.setDebugNode(self.debug_node)
        self.debug_np.hide()  # デフォルトでは非表示

    def setup_controls(self):
        """キー操作の設定"""
        self.accept("escape", sys.exit)
        self.accept("f1", self.toggle_debug)
        self.accept("r", self.reset)
        # その他のキー設定...

    def update_physics(self, task):
        """物理エンジンの更新"""
        dt = globalClock.getDt()
        self.bullet_world.doPhysics(dt)
        return task.cont

    def toggle_debug(self):
        """デバッグ表示の切り替え"""
        if self.debug_np.isHidden():
            self.debug_np.show()
        else:
            self.debug_np.hide()

    def reset(self):
        """世界をリセット"""
        # 全オブジェクトを削除
        for obj in self.objects:
            obj.remove()
        self.objects = []

        # 重力と地面をリセット
        self.bullet_world.setGravity(self.gravity_vector)
        self.world_node.setHpr(0, 0, 0)

    # オブジェクト追加メソッド
    def add_box(self, position=(0, 0, 0), scale=(1, 1, 1), color=(0.5, 0.5, 0.5), mass=1, color_alpha=1):
        """
        箱を追加

        Parameters:
        -----------
        position : tuple
            位置座標 (x, y, z)
        scale : tuple
            大きさ (幅, 奥行き, 高さ)
        color : tuple
            色 (赤, 緑, 青)
        mass : float
            質量

        Returns:
        --------
        Box: 作成された箱オブジェクト
        """
        box_data = {
            'type': 'box',
            'pos': position,
            'scale': scale,
            'color': color,
            'mass': mass,
            'color_alpha': color_alpha
        }
        box = Box(self, box_data)
        self.objects.append(box)
        return box

    def add_sphere(self, position=(0, 0, 0), scale=(1, 1, 1), color=(0.5, 0.5, 0.5), mass=1, color_alpha=1):
        """球を追加"""
        sphere_data = {
            'type': 'sphere',
            'pos': position,
            'scale': scale,
            'color': color,
            'mass': mass,
            'color_alpha': color_alpha
        }
        sphere = Sphere(self, sphere_data)
        self.objects.append(sphere)
        return sphere

    def add_cylinder(self, position=(0, 0, 0), scale=(1, 1, 1), color=(0.5, 0.5, 0.5), mass=1, color_alpha=1):
        """円柱を追加"""
        cylinder_data = {
            'type': 'cylinder',
            'pos': position,
            'scale': scale,
            'color': color,
            'mass': mass,
            'color_alpha': color_alpha
        }
        cylinder = Cylinder(self, cylinder_data)
        self.objects.append(cylinder)
        return cylinder

    def add(self, obj_type, **kwargs):
        """
        汎用オブジェクト追加メソッド

        Parameters:
        -----------
        obj_type : str
            'box', 'sphere', 'cylinder' などのオブジェクトタイプ
        **kwargs : dict
            オブジェクトのプロパティ

        Returns:
        --------
        作成されたオブジェクト
        """
        if obj_type == 'box':
            return self.add_box(**kwargs)
        elif obj_type == 'sphere':
            return self.add_sphere(**kwargs)
        # その他のタイプも同様に...

    def from_body_data(self, body_data):
        """
        body_dataリストからオブジェクトを作成

        Parameters:
        -----------
        body_data : list
            オブジェクト定義辞書のリスト
        """
        for data in body_data:
            obj_type = data.pop('type', 'box')
            self.add(obj_type, **data)
        return self

    def run(self):
        """シミュレーションを実行"""
        self.run()  # ShowBaseのrunメソッドを呼び出し
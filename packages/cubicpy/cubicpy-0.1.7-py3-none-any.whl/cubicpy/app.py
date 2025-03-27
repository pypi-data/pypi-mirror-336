from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import *
from . import (
    DEFAULT_GRAVITY_FACTOR,
    CameraControl, Axis, InputHandler,
    ModelManager, PhysicsEngine, WorldManager,
    ApiMethod
)


class CubicPyApp(ShowBase):
    """CubicPy アプリケーションのメインクラス"""
    GRAVITY_VECTOR = Vec3(0, 0, -9.81) * (10 ** -1)  # 重力ベクトル（10の1に補正）
    DEFAULT_WINDOW_SIZE = (900, 600)
    RESTITUTION = 0.5  # 反発係数
    FRICTION = 0.5  # 摩擦係数

    def __init__(self, code_file=None, gravity_factor=DEFAULT_GRAVITY_FACTOR, window_size=DEFAULT_WINDOW_SIZE):
        ShowBase.__init__(self)
        self.code_file = code_file
        self.initial_gravity_factor = gravity_factor
        self.window_size = window_size

        # ウィンドウ設定
        self.setup_window("CubicPy World", self.window_size)

        # カメラと座標軸
        CameraControl(self)
        Axis(self)

        # 各サブシステムの初期化
        self.model_manager = ModelManager(self)
        self.physics = PhysicsEngine(self)

        # APIメソッドの初期化（オブジェクト配置用）
        self.api = ApiMethod(self)

        # ワールド管理システムの初期化
        self.world_manager = WorldManager(self)

        # 入力ハンドラの設定
        self.input_handler = InputHandler(self)

        # 物理シミュレーションタスクの開始
        self.taskMgr.add(self.update_physics, 'update_physics')

        # コードファイルが指定されていれば、ワールド構築
        if code_file:
            self.world_manager.build_world()

    def setup_window(self, title, size):
        """ウィンドウ設定"""
        props = WindowProperties()
        props.setTitle(title)
        props.setSize(*size)
        self.win.requestProperties(props)

    def update_physics(self, task):
        """物理シミュレーションの更新"""
        dt = globalClock.getDt()
        self.physics.update(dt)
        return task.cont

    # ApiMethodクラスのメソッドを統合
    def add_cube(self, position=(0, 0, 0), scale=(1, 1, 1), color=(0.5, 0.5, 0.5), mass=1, color_alpha=1, remove=False):
        """箱を追加"""
        return self.api.add_cube(position, scale, color, mass, color_alpha)

    def add_sphere(self, position=(0, 0, 0), scale=(1, 1, 1), color=(0.5, 0.5, 0.5), mass=1, color_alpha=1, remove=False):
        """球を追加"""
        return self.api.add_sphere(position, scale, color, mass, color_alpha)

    def add_cylinder(self, position=(0, 0, 0), scale=(1, 1, 1), color=(0.5, 0.5, 0.5), mass=1, color_alpha=1, remove=False):
        """円柱を追加"""
        return self.api.add_cylinder(position, scale, color, mass, color_alpha)

    def add_ground(self, color=(0, 1, 0), color_alpha=0.3):
        """地面を追加"""
        return self.api.add_ground(color, color_alpha)

    def add(self, obj_type, **kwargs):
        """汎用オブジェクト追加"""
        return self.api.add(obj_type, **kwargs)

    def from_body_data(self, body_data):
        """オブジェクトデータからボディを構築"""
        self.api.from_body_data(body_data)

    def reset(self):
        """オブジェクトをリセット"""
        # ワールドを再構築
        self.world_manager.rebuild_from_api_data()

    # 既存の委譲メソッド - WorldManagerへ転送
    def tilt_ground(self, dx, dy):
        self.world_manager.tilt_ground(dx, dy)

    def toggle_debug(self):
        self.physics.toggle_debug()

    def change_gravity(self, value):
        # 物理エンジンの重力を変更
        self.physics.change_gravity(value)
        # そしてワールドを再構築  # この行は削除すると、地面を傾けても崩壊しない
        self.world_manager.rebuild()

    def reset_all(self):
        """すべてをリセット"""
        self.physics.reset_gravity()
        self.world_manager.reset_rotation()
        self.world_manager.rebuild()

    # メソッドをオーバーライド
    def run(self):
        """世界を構築して実行"""
        if self.code_file is None:
            # APIからのオブジェクトデータでワールドを構築
            self.world_manager.build_from_api_data()

        # アプリを実行
        super().run()

    # 選択したオブジェクトを削除
    def remove_selected(self):
        self.world_manager.remove_selected()

    # 選択したオブジェクトを発射
    def launch_objects(self):
        """初速度ベクトルが設定されたオブジェクトを発射"""
        self.world_manager.launch_objects()

    @property
    def world_node(self):
        """ワールドノードへの参照を提供"""
        return self.world_manager.get_world_node()
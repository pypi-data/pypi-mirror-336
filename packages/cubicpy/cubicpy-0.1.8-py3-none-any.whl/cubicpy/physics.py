from panda3d.bullet import BulletWorld, BulletDebugNode


class PhysicsEngine:
    """物理シミュレーション管理クラス"""

    def __init__(self, app):
        self.app = app
        self.gravity_vector = app.GRAVITY_VECTOR * app.initial_gravity_factor

        # Bulletワールドを作成
        self.bullet_world = BulletWorld()

        # デバッグ表示で物理オブジェクトの形状を表示
        self.setup_debug()

        # 重力の設定
        print(f'Initial Gravity: {self.gravity_vector}')
        self.bullet_world.setGravity(self.gravity_vector)

    def setup_debug(self):
        """デバッグ表示の設定"""
        self.debug_node = BulletDebugNode("colliderDebug")
        self.debug_np = self.app.render.attachNewNode(self.debug_node)
        self.bullet_world.setDebugNode(self.debug_node)
        self.debug_np.show()

    def toggle_debug(self):
        """デバッグ表示の切り替え"""
        if self.debug_np.isHidden():
            self.debug_np.show()
        else:
            self.debug_np.hide()

    def update(self, dt):
        """物理シミュレーションの更新"""
        self.bullet_world.doPhysics(dt)

    def change_gravity(self, value):
        """重力の変更"""
        if value != 0:  # 0でない場合のみ重力を変更
            self.gravity_vector *= value
            print(f'Change Gravity: {self.gravity_vector}')
            self.bullet_world.setGravity(self.gravity_vector)
            # 注意：ここではreset_buildを呼び出さない
            # 代わりにappに通知し、appが適切な処理を行う

            # 物理エンジンを即座に更新
            self.bullet_world.doPhysics(0)

    def reset_gravity(self):
        """重力を初期状態に戻す"""
        self.gravity_vector = self.app.GRAVITY_VECTOR * self.app.initial_gravity_factor
        print(f'Reset Gravity: {self.gravity_vector}')
        self.bullet_world.setGravity(self.gravity_vector)

        # 物理エンジンを即座に更新
        self.bullet_world.doPhysics(0)
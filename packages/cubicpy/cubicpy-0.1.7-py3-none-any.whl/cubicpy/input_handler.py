import sys


class InputHandler:
    """キー入力処理クラス"""

    def __init__(self, app):
        self.app = app

        # キー入力の登録
        self.setup_keys()

    def setup_keys(self):
        """キー入力の設定"""
        self.app.accept('escape', sys.exit)
        # デバッグ表示の切り替え
        self.app.accept('z', self.app.toggle_debug)
        # 重力の変更
        self.app.accept('f', self.app.change_gravity, [0.1])
        self.app.accept('g', self.app.change_gravity, [10])
        # ワールドのリセット
        self.app.accept('r', self.app.reset_all)
        # 地面の傾き
        self.app.accept("w", self.app.tilt_ground, [-1, 0])  # X軸 (前傾)
        self.app.accept("s", self.app.tilt_ground, [1, 0])  # X軸 (後傾)
        self.app.accept("a", self.app.tilt_ground, [0, -1])  # Y軸 (左傾)
        self.app.accept("d", self.app.tilt_ground, [0, 1])  # Y軸 (右傾)
        # オブジェクトの削除
        self.app.accept('x', self.app.remove_selected)
        # オブジェクトの発射
        self.app.accept('space', self.app.launch_objects)
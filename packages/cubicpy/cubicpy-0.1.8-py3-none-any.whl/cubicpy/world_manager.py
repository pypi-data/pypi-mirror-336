from panda3d.core import Vec3
from . import Cube, Sphere, Cylinder, SafeExec


class WorldManager:
    """ワールドとオブジェクト管理クラス"""

    def __init__(self, app):
        self.app = app
        self.body_objects = []

        # 回転状態の初期化
        self.tilt_x = 0
        self.tilt_y = 0
        self.tilt_speed = 5
        self.target_tilt_x = 0
        self.target_tilt_y = 0
        self.tilt_step = 0
        self.max_tilt_frames = 10

        # ワールドのルートノード
        self.world_node = self.app.render.attachNewNode("world_node")

    def tilt_ground(self, dx, dy):
        """目標の傾きを設定し、徐々に傾ける"""
        self.target_tilt_x = self.tilt_x + dx * self.tilt_speed
        self.target_tilt_y = self.tilt_y + dy * self.tilt_speed
        print(f'Target Tilt: {self.target_tilt_x}, {self.target_tilt_y}')
        self.tilt_step = 0
        self.app.taskMgr.add(self.smooth_tilt_update, 'smooth_tilt_update')

    def smooth_tilt_update(self, task):
        """徐々に傾きを変更するタスク"""
        if self.tilt_step >= self.max_tilt_frames:
            # 重力の再設定
            self.app.change_gravity(10)
            return task.done

        # 徐々に目標角度に近づける
        alpha = (self.tilt_step + 1) / self.max_tilt_frames
        self.tilt_x = (1 - alpha) * self.tilt_x + alpha * self.target_tilt_x
        self.tilt_y = (1 - alpha) * self.tilt_y + alpha * self.target_tilt_y

        # ワールドの回転を適用
        self.world_node.setHpr(0, self.tilt_x, self.tilt_y)

        self.tilt_step += 1
        return task.cont

    def reset_rotation(self):
        """回転をリセット"""
        self.tilt_x = 0
        self.tilt_y = 0
        self.world_node.setHpr(0, 0, 0)

    def build_body_data(self, body_data):
        """オブジェクトデータからボディを構築"""
        for body in body_data:
            if body['type'] == 'cube':
                body_object = Cube(self.app, body)
            elif body['type'] == 'sphere':
                body_object = Sphere(self.app, body)
            elif body['type'] == 'cylinder':
                body_object = Cylinder(self.app, body)
            else:
                body_object = Cube(self.app, body)
            self.body_objects.append({'type': body['type'], 'object': body_object})

    def rebuild(self):
        """ワールドを再構築"""
        # 既存のオブジェクトを削除
        self.clear_objects()

        # コードファイルがある場合はそのデータを使用
        if self.app.code_file:
            self.build_world()
        else:
            # APIデータからワールドを再構築
            self.build_from_api_data()

    def get_world_node(self):
        """ワールドノードを取得"""
        return self.world_node

    def build_world(self):
        """コードファイルからワールドを構築"""
        if self.app.code_file:
            safe_exec = SafeExec(self.app.code_file)
            body_data = safe_exec.run()
        else:
            body_data = []

        # 地面を追加（必要な場合）
        self.add_default_ground(body_data)

        # 建物を構築
        self.build_body_data(body_data)

        # 物理エンジンを即座に更新
        self.app.physics.bullet_world.doPhysics(0)

    def build_from_api_data(self):
        """APIデータからワールドを構築"""
        # APIからのオブジェクトデータを取得
        body_data = self.app.api.get_object_data()

        # 地面を追加（必要な場合）
        self.add_default_ground(body_data)

        # 建物を構築
        self.build_body_data(body_data)

        # 物理エンジンを即座に更新
        self.app.physics.bullet_world.doPhysics(0)

    @staticmethod
    def add_default_ground(body_data):
        """デフォルトの地面を追加（必要な場合）"""
        # 地面がまだ存在しない場合は追加
        has_ground = any(data.get('mass', 1) == 0 and
                          data.get('type') == 'cube' and
                          abs(data.get('scale', (1, 1, 1))[0]) > 500
                          for data in body_data)

        if not has_ground:
            body_data.append({
                'type': 'cube',
                'pos': (-500, -500, -1),
                'scale': (1000, 1000, 1),
                'color': (0, 1, 0),
                'mass': 0,
                'color_alpha': 0.3
            })

    def rebuild_from_api_data(self):
        """APIデータからワールドを再構築"""
        # 既存のオブジェクトを削除
        self.clear_objects()

        # APIデータでワールドを再構築
        self.build_from_api_data()

    def clear_objects(self):
        """すべてのオブジェクトを削除"""
        for body in self.body_objects:
            body['object'].remove()

        self.body_objects = []

    def remove_selected(self):
        """選択したオブジェクトを削除"""
        for body in self.body_objects:
            remove_selected = getattr(body['object'], 'remove_selected', False)
            if remove_selected:
                body['object'].remove()
                self.body_objects.remove(body)

                # 物理エンジンを即座に更新  # TODO 削除の毎回実行すべきか？
                self.app.physics.bullet_world.doPhysics(0)

    def launch_objects(self):
        """初速度ベクトルが設定されたオブジェクトを発射"""
        for body in self.body_objects:
            obj = body['object']
            if hasattr(obj, 'vec') and obj.vec != Vec3(0, 0, 0):
                obj.apply_velocity()
                print(f"オブジェクトを速度 {obj.vec} で発射しました")

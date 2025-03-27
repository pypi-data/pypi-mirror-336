from panda3d.core import Vec3, TransparencyAttrib
from pkg_resources import resource_filename


class ModelManager:
    """3Dモデル管理クラス"""

    def __init__(self, app):
        self.app = app

        # 形状キャッシュ
        self.cube_shapes = {}
        self.sphere_shapes = {}
        self.cylinder_shapes = {}

        # Cube Model
        self.cube_model = self.load_cube_model()

        # Sphere Model
        self.sphere_model = self.load_sphere_model()

        # Cylinder Model
        self.cylinder_model = self.load_cylinder_model()

    def load_cube_model(self):
        """ボックスモデルのロード"""
        model = self.app.loader.loadModel('models/box.egg')
        model.setPos(-0.5, -0.5, -0.5)  # モデルの中心を原点に
        model.setScale(1, 1, 1)
        model.setTextureOff(1)
        model.flattenLight()
        return model

    def load_sphere_model(self):
        """球体モデルのロード"""
        model = self.app.loader.loadModel('misc/sphere.egg')
        model.setScale(0.5)
        model.setTextureOff(1)
        model.flattenLight()
        return model

    def load_cylinder_model(self):
        """円柱モデルのロード"""
        model_file = resource_filename('cubicpy', 'models/cylinder48.egg')
        model = self.app.loader.loadModel(model_file)
        model.setPos(0, 0, -0.5)  # モデルの中心を原点に
        model.setScale(1, 1, 1)
        model.setTextureOff(1)
        model.flattenLight()
        return model
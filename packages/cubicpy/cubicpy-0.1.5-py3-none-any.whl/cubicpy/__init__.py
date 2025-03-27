DEFAULT_GRAVITY_FACTOR = 1

from .base_point import get_position_offset
from .box import Box
from .sphere import Sphere
from .cylinder import Cylinder
from .camera import CameraControl
from .axis import Axis
from .geom_utils import *
from .safe_exec import SafeExec
from .input_handler import InputHandler
from .model_manager import ModelManager
from .physics import PhysicsEngine
from .world_manager import WorldManager
from .api_method import ApiMethod
from .app import CubicPyApp

# サンプル関連機能をエクスポート
from .examples import get_sample_path, list_samples


# 簡単にサンプルを実行するための補助関数
def run_sample(sample_name, gravity_factor=DEFAULT_GRAVITY_FACTOR):
    """指定したサンプルを実行する

    Args:
        sample_name: サンプル名（.pyなしのファイル名）
        gravity_factor: 重力係数
    """
    app = CubicPyApp(get_sample_path(sample_name), gravity_factor=gravity_factor)
    app.run()

__version__ = "0.1.5"
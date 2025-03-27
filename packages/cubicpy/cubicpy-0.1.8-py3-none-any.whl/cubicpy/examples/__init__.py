import os
import importlib.resources as resources
import pkgutil
import re


def _discover_samples():
    """サンプルファイル一覧を自動検出する"""
    samples = []

    # このパッケージ内のすべてのモジュールを取得
    package_path = os.path.dirname(__file__)
    for _, module_name, is_pkg in pkgutil.iter_modules([package_path]):
        # パッケージでなく、.pyファイルのみを対象
        if not is_pkg and module_name.endswith('_sample'):
            samples.append(module_name)

    return sorted(samples)


# サンプル一覧を自動検出
SAMPLES = _discover_samples()


def get_sample_path(sample_name):
    """サンプルファイルの完全パスを返す

    Args:
        sample_name: サンプル名（.pyなしのファイル名）

    Returns:
        str: サンプルファイルの完全パス
    """
    if not sample_name.endswith('.py'):
        sample_name = f"{sample_name}.py"

    try:
        with resources.path(__package__, sample_name) as path:
            return str(path)
    except FileNotFoundError:
        raise ValueError(f"サンプル '{sample_name}' が見つかりません。利用可能なサンプル: {list_samples()}")


def list_samples():
    """利用可能なサンプル一覧を返す"""
    return SAMPLES


# 開発時のテスト用
if __name__ == "__main__":
    print("検出されたサンプル一覧:")
    for sample in SAMPLES:
        print(f" - {sample}")
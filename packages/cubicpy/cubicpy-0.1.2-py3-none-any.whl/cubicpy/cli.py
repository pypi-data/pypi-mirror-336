#!/usr/bin/env python
"""
CubicPy コマンドラインインターフェース
キューブを積み上げて物理シミュレーションを行う子供向けPython学習ツール
"""
import argparse
import os
import sys
from cubicpy import CubicPyApp, list_samples, get_sample_path


def main():
    """コマンドラインエントリーポイント"""
    # コマンドライン引数のパーサーを作成
    parser = argparse.ArgumentParser(
        description='CubicPy - 子供向けPython物理シミュレーション',
        epilog='例: cubicpy -e box_tower_sample または cubicpy my_script.py'
    )
    parser.add_argument('--example', '-e',
                        help='実行するサンプル名（例: box_tower_sample）')
    parser.add_argument('--list', '-l', action='store_true',
                        help='利用可能なサンプル一覧を表示')
    parser.add_argument('--gravity', '-g', type=int, default=-4,
                        help='重力係数（デフォルト: -4）')
    parser.add_argument('file', nargs='?',
                        help='実行するPythonファイル（オプション）')

    args = parser.parse_args()

    # サンプル一覧の表示
    if args.list:
        print("利用可能なサンプル:")
        for sample in list_samples():
            print(f"  {sample}")
        return 0

    # ファイルパスの決定
    if args.example:
        try:
            file_path = get_sample_path(args.example)
            print(f"サンプル '{args.example}' を実行します")
        except ValueError as e:
            print(f"エラー: {e}")
            return 1
    elif args.file:
        # ユーザー指定のファイル
        file_path = args.file

        # ファイルの存在確認
        if not os.path.exists(file_path):
            print(f"エラー: ファイル '{file_path}' が見つかりません")
            return 1

        # 安全なパスに変換
        file_path = os.path.abspath(file_path)
        print(f"ファイル '{file_path}' を実行します")
    else:
        # デフォルトサンプル - 最初のサンプルを使用
        default_sample = list_samples()[0] if list_samples() else 'box_tower_sample'
        try:
            file_path = get_sample_path(default_sample)
            print(f"デフォルトサンプル '{default_sample}' を実行します")
        except ValueError as e:
            print(f"エラー: デフォルトサンプルが見つかりません: {e}")
            return 1

    try:
        # アプリを起動
        app = CubicPyApp(file_path, gravity_factor=args.gravity)
        app.run()
    except Exception as e:
        print(f"エラー: アプリケーションの実行中にエラーが発生しました: {e}")
        return 1

    return 0


# モジュールとして直接実行された場合のエントリーポイント
if __name__ == '__main__':
    sys.exit(main())
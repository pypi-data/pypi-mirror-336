#!/usr/bin/env python
"""
CubicPy コマンドラインインターフェース
キューブを積み上げて物理シミュレーションを行う子供向けPython学習ツール
"""
import argparse
import os
import sys
import locale
import random
from cubicpy import CubicPyApp, list_samples, get_sample_path, DEFAULT_GRAVITY_FACTOR, __version__

# 言語に応じたメッセージ
MESSAGES = {
    'ja': {
        'description': 'CubicPy - コードで物理オブジェクトを配置・構築する3Dプログラミング学習アプリ',
        'epilog': '例: cubicpy -e cube_tower_sample または cubicpy my_script.py',
        'example_help': '実行するサンプル名（例: cube_tower_sample）',
        'list_help': '利用可能なサンプル一覧を表示',
        'gravity_help': '重力係数（デフォルト: 0）',
        'window_size_help': 'ウィンドウサイズをカンマ区切りで指定（例: 1280,720）デフォルト: 900,600',
        'file_help': '実行するPythonファイル（オプション）',
        'version_help': 'バージョン情報を表示',
        'version_info': 'CubicPy バージョン {0}',
        'available_samples': '利用可能なサンプル:',
        'running_sample': "サンプル '{0}' を実行します",
        'error_sample_not_found': "エラー: {0}",
        'error_file_not_found': "エラー: ファイル '{0}' が見つかりません",
        'running_file': "ファイル '{0}' を実行します",
        'running_default_sample': "デフォルトサンプル '{0}' を実行します",
        'error_default_sample': "エラー: デフォルトサンプルが見つかりません: {0}",
        'error_application': "エラー: アプリケーションの実行中にエラーが発生しました: {0}",
        'error_window_size': "エラー: ウィンドウサイズの形式が無効です。例: 1280,720",
        'code_preview': "--- サンプルコード ---",
        'code_preview_end': "--- コード終了 ---"
    },
    'en': {
        'description': 'CubicPy - 3D programming learning app: place physics objects with code and build',
        'epilog': 'Example: cubicpy -e cube_tower_sample or cubicpy my_script.py',
        'example_help': 'Sample name to run (e.g. cube_tower_sample)',
        'list_help': 'Display list of available samples',
        'gravity_help': 'Gravity factor (default: 0)',
        'window_size_help': 'Window size as comma-separated values (e.g. 1280,720) default: 900,600',
        'file_help': 'Python file to run (optional)',
        'version_help': 'Display version information',
        'version_info': 'CubicPy version {0}',
        'available_samples': 'Available samples:',
        'running_sample': "Running sample '{0}'",
        'error_sample_not_found': "Error: {0}",
        'error_file_not_found': "Error: File '{0}' not found",
        'running_file': "Running file '{0}'",
        'running_default_sample': "Running default sample '{0}'",
        'error_default_sample': "Error: Default sample not found: {0}",
        'error_application': "Error: An error occurred while running the application: {0}",
        'error_window_size': "Error: Invalid window size format. Example: 1280,720",
        'code_preview': "--- Sample Code ---",
        'code_preview_end': "--- End of Code ---"
    }
}


def get_system_language():
    """システムの言語を取得する"""
    try:
        language, _ = locale.getdefaultlocale()
        if language and language.startswith('ja'):
            return 'ja'
    except:
        pass
    return 'en'


def display_code(file_path, lang):
    """コードファイルの内容をコンソールに表示する"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            code_content = file.read()

        print(f"\n{MESSAGES[lang]['code_preview']}")
        print(code_content)
        print(f"{MESSAGES[lang]['code_preview_end']}\n")
    except Exception as e:
        print(f"Error reading code file: {e}")


def parse_window_size(size_str, lang):
    """ウィンドウサイズの文字列をタプルに変換する"""
    try:
        width, height = map(int, size_str.split(','))
        return (width, height)
    except ValueError:
        print(MESSAGES[lang]['error_window_size'])
        return None


def main():
    """コマンドラインエントリーポイント"""
    # システムの言語を取得
    lang = get_system_language()
    msgs = MESSAGES[lang]

    # コマンドライン引数のパーサーを作成
    parser = argparse.ArgumentParser(
        description=msgs['description'],
        epilog=msgs['epilog']
    )
    parser.add_argument('--example', '-e',
                        help=msgs['example_help'])
    parser.add_argument('--list', '-l', action='store_true',
                        help=msgs['list_help'])
    parser.add_argument('--gravity', '-g', type=float, default=DEFAULT_GRAVITY_FACTOR,
                        help=msgs['gravity_help'])
    parser.add_argument('--window-size', '-w', default="900,600",
                        help=msgs['window_size_help'])
    parser.add_argument('--version', '-v', action='store_true',
                        help=msgs['version_help'])
    parser.add_argument('file', nargs='?',
                        help=msgs['file_help'])

    args = parser.parse_args()

    # バージョン情報の表示
    if args.version:
        print(msgs['version_info'].format(__version__))
        return 0

    # ウィンドウサイズのパース
    window_size = parse_window_size(args.window_size, lang)
    if window_size is None:
        return 1

    # サンプル一覧の表示
    if args.list:
        print(msgs['available_samples'])
        for sample in list_samples():
            print(f"  {sample}")
        return 0

    # ファイルパスの決定
    if args.example:
        try:
            file_path = get_sample_path(args.example)
            print(msgs['running_sample'].format(args.example))
            # サンプルコードを表示
            display_code(file_path, lang)
        except ValueError as e:
            print(msgs['error_sample_not_found'].format(e))
            return 1
    elif args.file:
        # ユーザー指定のファイル
        file_path = args.file

        # ファイルの存在確認
        if not os.path.exists(file_path):
            print(msgs['error_file_not_found'].format(file_path))
            return 1

        # 安全なパスに変換
        file_path = os.path.abspath(file_path)
        print(msgs['running_file'].format(file_path))
    else:
        # デフォルトサンプル - 最初のサンプルを使用
        default_sample = random.choice(list_samples()) if list_samples() else 'cube_tower_sample'
        try:
            file_path = get_sample_path(default_sample)
            print(msgs['running_default_sample'].format(default_sample))
            # サンプルコードを表示
            display_code(file_path, lang)
        except ValueError as e:
            print(msgs['error_default_sample'].format(e))
            return 1

    try:
        # アプリを起動
        app = CubicPyApp(file_path, gravity_factor=args.gravity, window_size=window_size)
        app.run()
    except Exception as e:
        print(msgs['error_application'].format(e))
        return 1

    return 0


# モジュールとして直接実行された場合のエントリーポイント
if __name__ == '__main__':
    sys.exit(main())
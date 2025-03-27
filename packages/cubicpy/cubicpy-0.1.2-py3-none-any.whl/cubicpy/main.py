from . import CubicPyApp

def main():
    """コマンドラインエントリーポイント"""
    import sys
    import os

    # コマンドライン引数からPythonファイルのパスを取得
    if len(sys.argv) > 1:
        user_code_file = sys.argv[1]

        # ファイルの存在確認
        if not os.path.exists(user_code_file):
            print(f"エラー: ファイル '{user_code_file}' が見つかりません")
            sys.exit(1)

        # 安全なパスに変換
        user_code_file = os.path.abspath(user_code_file)
    else:
        # 引数がない場合はデフォルトのサンプルコードを使用
        from pkg_resources import resource_filename
        user_code_file = resource_filename('cubicpy', 'examples/box_building_sample.py')
        print(f"サンプルコード {user_code_file} を使用します")

    # アプリケーションを実行
    app = CubicPyApp(user_code_file, gravity_factor=-6)
    app.run()


if __name__ == '__main__':
    main()
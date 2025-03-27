import math
import numpy as np

class SafeExec:
    def __init__(self, user_code_file):
        self.file_path = user_code_file
        self.safe_globals = {
            "__builtins__": {
                "range": range,
                "len": len,
                "abs": abs,
                "min": min,
                "max": max,
                "sum": sum,
                "int": int,
                "float": float,
            },
            "sin": math.sin, "cos": math.cos, "tan": math.tan, "degrees": math.degrees,
            "asin": math.asin, "acos": math.acos, "atan": math.atan, "atan2": math.atan2,
            "sqrt": math.sqrt, "pi": math.pi, "exp": math.exp,
            "log": math.log, "pow": math.pow, "fabs": math.fabs,
            "ceil": math.ceil, "floor": math.floor,
            "math.sin": math.sin, "math.cos": math.cos, "math.tan": math.tan, "math.degrees": math.degrees,
            "math.asin": math.asin, "math.acos": math.acos, "math.atan": math.atan, "math.atan2": math.atan2,
            "math.sqrt": math.sqrt, "math.pi": math.pi, "math.exp": math.exp,
            "math.log": math.log, "math.pow": math.pow, "math.fabs": math.fabs,
            "math.ceil": math.ceil, "math.floor": math.floor,
            "np": np,
        }

    def run(self):
        safe_locals = {}

        # ファイルからユーザーコードを読み込む
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                user_code_lines = f.readlines()  # すべての行をリストとして読み込む

            # "import" または "from" で始まる行を削除
            filtered_code_lines = [line for line in user_code_lines if not line.strip().startswith(("import", "from"))]

            # 改行を含めて結合
            user_code = "".join(filtered_code_lines)

        except FileNotFoundError:
            print(f"Error: ファイル '{self.file_path}' が見つかりません")
            user_code = ""
        except Exception as e:
            print(f"Error: ファイルを読み込めません ({e})")
            user_code = ""

        # exec() の実行
        try:
            exec(user_code, self.safe_globals, safe_locals)
            body_data = safe_locals.get("body_data", [])
            return body_data
        except Exception as e:
            print(f"Execution error: {e}")
            return []

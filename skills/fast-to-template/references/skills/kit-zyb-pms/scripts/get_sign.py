import base64
import hashlib
import os
import time

def get_sign(params: dict) -> str:
    """
    验签算法：
    1. 对参数字典按 key 排序
    2. 用 & 拼接为 key=value 字符串
    3. 转为大写
    4. 取 MD5 十六进制摘要（小写）
    """
    sorted_str = "&".join(f"{k}={v}" for k, v in sorted(params.items()))
    secret_file = os.path.join(os.path.dirname(__file__), ".pms_secret")
    try:
        with open(secret_file, "r") as f:
            encoded_secret = f.read().strip()
    except FileNotFoundError:
        raise RuntimeError(".pms_secret file not found")
    secret = base64.b64decode(encoded_secret).decode("utf-8")
    sorted_str += f"&secret={secret}"
    sign = hashlib.md5(sorted_str.encode("utf-8")).hexdigest()
    sign = sign.upper()
    return sign


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python get_sign.py '{\"key1\":\"val1\",\"key2\":\"val2\"}'")
        sys.exit(1)

    params = json.loads(sys.argv[1])
    print(get_sign(params))

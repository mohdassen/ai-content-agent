import json

from src.readiness import platform_readiness


if __name__ == "__main__":
    print(json.dumps(platform_readiness(), ensure_ascii=False, indent=2))

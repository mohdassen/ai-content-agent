import json

from src.telegram_decision import poll_latest_decision


def main() -> None:
    result = poll_latest_decision()
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()

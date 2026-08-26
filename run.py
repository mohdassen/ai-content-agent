import argparse

from src.pipeline import build_demo_package, save_package


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Content Agent")
    parser.add_argument("--demo", action="store_true", help="Run safe local demo pipeline")
    args = parser.parse_args()

    if not args.demo:
        parser.error("Use --demo until production providers are configured")

    package = build_demo_package()
    path = save_package(package)
    print(f"Content package created: {path}")
    print(f"Viral score: {package['viral_score']}/10")
    print(f"Quality: {package['quality']['score']}/10")
    print("Publishing remains disabled until credentials and approval are configured.")


if __name__ == "__main__":
    main()

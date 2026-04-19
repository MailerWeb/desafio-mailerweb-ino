from __future__ import annotations

import argparse
import logging

from app.worker.processor import OutboxWorker


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the outbox worker")
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run a single polling cycle and exit",
    )
    return parser.parse_args()


def main() -> None:
    configure_logging()
    args = parse_args()
    worker = OutboxWorker()

    if args.once:
        worker.run_once()
        return

    worker.run_forever()


if __name__ == "__main__":
    main()

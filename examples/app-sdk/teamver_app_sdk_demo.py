#!/usr/bin/env python3
"""TeamverAppClient / TeamverM2MClient 예시 (teamver-app-sdk-python).

  python teamver_app_sdk_demo.py --help
  python teamver_app_sdk_demo.py dry-run
  python teamver_app_sdk_demo.py m2m-health

Live bootstrap/me: examples/python-sdk-cli/smoke.py
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys

from _demo_help import DESIGN_EPILOG

from teamver_app_sdk import TeamverAppClient, TeamverM2MClient
from teamver_app_sdk.config import TeamverAppConfig, TeamverM2MConfig


def _print_json(data: object) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2, default=str))


async def cmd_dry_run(_: argparse.Namespace) -> None:
    app_cfg = TeamverAppConfig.from_env()
    m2m_cfg = TeamverM2MConfig.from_env()
    _print_json(
        {
            "TeamverAppClient": {
                "api_base_url": app_cfg.api_base_url,
                "app_key": app_cfg.app_key,
            },
            "TeamverM2MClient": {"api_base_url": m2m_cfg.api_base_url},
        }
    )


async def cmd_m2m_health(_: argparse.Namespace) -> None:
    async with TeamverM2MClient.from_env() as client:
        data = await client.health()
    _print_json(data)


async def cmd_bootstrap(args: argparse.Namespace) -> None:
    token = (args.token or os.getenv("TEAMVER_ACCESS_TOKEN") or "").strip()
    if not token:
        print("Need --token or TEAMVER_ACCESS_TOKEN", file=sys.stderr)
        sys.exit(2)
    async with TeamverAppClient.from_env(app_key=args.app_key) as client:
        data = await client.auth.get_bootstrap(access_token=token)
    _print_json(data.model_dump() if hasattr(data, "model_dump") else data)


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="teamver_app_sdk_demo.py",
        description="teamver-app-sdk — AI App BE용 Main BE 클라이언트",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=DESIGN_EPILOG + "\nLive smoke: examples/python-sdk-cli/smoke.py",
    )
    parser.add_argument("--app-key", default=os.getenv("TEAMVER_APP_KEY", "docs"))
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("dry-run", help="Print App/M2M config from env")
    p.set_defaults(func=cmd_dry_run)

    p = sub.add_parser("m2m-health", help="M2M health probe")
    p.set_defaults(func=cmd_m2m_health)

    p = sub.add_parser("bootstrap", help="GET internal/apps/{app_key}/bootstrap")
    p.add_argument("--token", help="User access token")
    p.set_defaults(func=cmd_bootstrap)

    args = parser.parse_args()
    asyncio.run(args.func(args))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

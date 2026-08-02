#!/usr/bin/env python3
"""TeamverMailAgentClient 예시 (teamver-mail-agent-python).

  python teamver_mail_agent_demo.py --help
  python teamver_mail_agent_demo.py dry-run
  python teamver_mail_agent_demo.py ops-health
"""

from __future__ import annotations

import argparse
import asyncio
import json

from _demo_help import DESIGN_EPILOG

from teamver_mail_agent import TeamverMailAgentClient
from teamver_mail_agent.config import TeamverMailAgentConfig


def _print_json(data: object) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2, default=str))


async def cmd_dry_run(_: argparse.Namespace) -> None:
    cfg = TeamverMailAgentConfig.from_env()
    _print_json(
        {
            "client": "TeamverMailAgentClient",
            "mail_api_base": cfg.api_base_url,
            "agent_token_set": bool(getattr(cfg, "agent_token", None) or getattr(cfg, "mail_agent_token", None)),
            "categories": ["agent_api", "agent_processing", "agent_events", "agent_reply", "ops", "internal_m2m"],
        }
    )


async def cmd_ops_health(_: argparse.Namespace) -> None:
    async with TeamverMailAgentClient.from_env() as client:
        data = await client.ops.health()
    _print_json(data)


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="teamver_mail_agent_demo.py",
        description="teamver-mail-agent — Mail BE Agent API client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=DESIGN_EPILOG,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("dry-run", help="Print Mail agent config from env")
    p.set_defaults(func=cmd_dry_run)

    p = sub.add_parser("ops-health", help="GET mail ops health")
    p.set_defaults(func=cmd_ops_health)

    args = parser.parse_args()
    asyncio.run(args.func(args))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

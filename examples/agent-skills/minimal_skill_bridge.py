#!/usr/bin/env python3
"""OpenClaw + Teamver skills minimal example (install from PyPI)."""

from __future__ import annotations

import asyncio
import os

from teamver_agent_sdk import TeamverAgent, TeamverAgentConfig
from teamver_openclaw_adapter import OpenClawToolBridge


async def main() -> None:
    agent = TeamverAgent(TeamverAgentConfig.from_env())
    bridge = OpenClawToolBridge(agent)
    print(f"tools={len(bridge.list_tools())}")
    if os.getenv("TEAMVER_RUN_HEARTBEAT_TOOL") == "1":
        out = await bridge.dispatch(
            "teamver_heartbeat",
            {"operational_status": "idle", "active_job_count": 0},
        )
        print(out)
    await agent.aclose()


if __name__ == "__main__":
    asyncio.run(main())

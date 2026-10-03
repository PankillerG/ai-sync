import argparse
import sys
from pathlib import Path

from ai_sync import (
    config,
    commands,
)
from ai_sync.entities import ENTITY_TYPE_VALUES
from ai_sync.providers import PROVIDER_NAME_VALUES


DIR_HELP = (
    "Scope root: your home directory (default) deploys from ~/.config/ai-sync to user-level configs, "
    "any other directory is a project that deploys from <dir>/.ai-sync into it"
)


def main() -> None:
    parser = argparse.ArgumentParser(prog="ai-sync", description="Sync agent entities across AI providers")
    sub = parser.add_subparsers(dest="command")

    # init
    p_init = sub.add_parser("init", help="Create a new entity from template")
    p_init.add_argument("entity_type", choices=ENTITY_TYPE_VALUES)
    p_init.add_argument("entity_name", help="Entity name")
    p_init.add_argument("--dir", type=Path, default=config.DEFAULT_WORK_DIR, help=DIR_HELP)

    # deploy
    p_deploy = sub.add_parser("deploy", help="Generate provider-specific files and deploy them")
    p_deploy.add_argument("--dir", type=Path, default=config.DEFAULT_WORK_DIR, help=DIR_HELP)
    p_deploy.add_argument(
        "-p",
        "--providers",
        nargs="+",
        choices=PROVIDER_NAME_VALUES,
        default=PROVIDER_NAME_VALUES,
        help="Providers to deploy for (default: all)",
    )

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "init":
            commands.init(args)

        elif args.command == "deploy":
            commands.deploy(args)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

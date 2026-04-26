import argparse
import sys
from pathlib import Path

from ai_sync import (
    config,
    commands,
)
from ai_sync.entities import ENTITY_TYPE_VALUES


def main() -> None:
    parser = argparse.ArgumentParser(prog="ai-sync", description="Sync agent entities across AI providers")
    parser.add_argument("--dir", type=Path, default=config.DEFAULT_WORK_DIR, help="Working directory")
    sub = parser.add_subparsers(dest="command")

    # init
    p_init = sub.add_parser("init", help="Create a new entity from template")
    p_init.add_argument("entity_type", choices=ENTITY_TYPE_VALUES)
    p_init.add_argument("entity_name", help="Entity name")

    # generate
    sub.add_parser("generate", help="Generate provider-specific files")

    # deploy
    sub.add_parser("deploy", help="Deploy generated files to provider directories")

    # update
    p_update = sub.add_parser("update", help="Regenerate derived configs from current state")
    update_sub = p_update.add_subparsers(dest="update_target")
    update_sub.add_parser("deploy-config", help="Update deploy.yaml from generated output")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "init":
            commands.init(args)

        elif args.command == "generate":
            commands.generate(args)

        elif args.command == "update":
            if args.update_target == "deploy-config":
                commands.update_deploy_config(args)

        elif args.command == "deploy":
            commands.deploy(args)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

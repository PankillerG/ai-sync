import argparse

from ai_sync import actions
from ai_sync.workspace import Workspace


def run(args: argparse.Namespace) -> None:
    ws = Workspace(root=args.dir)
    actions.update_deploy_config(ws)
    print(f"Updated {ws.deploy_yaml_file}")

import argparse

from ai_sync import actions
from ai_sync.workspace import Workspace


def run(args: argparse.Namespace) -> None:
    ws = Workspace(root=args.dir)
    actions.deploy(ws)
    print("Deploy complete.")

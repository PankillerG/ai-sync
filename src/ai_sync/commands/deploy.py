import argparse

from ai_sync import actions
from ai_sync.commands import utils
from ai_sync.providers import ProviderName
from ai_sync.workspace import Workspace


def run(args: argparse.Namespace) -> None:
    work_dir = utils.resolve_work_dir(args.dir)
    scope = utils.get_scope(work_dir)
    ws = Workspace(root=utils.get_workspace_root(work_dir, scope))
    providers = [ProviderName(provider) for provider in args.providers]

    actions.deploy(ws, work_dir, scope, providers)
    print(f"Deployed {ws.root} to {scope} scope at {work_dir} for: {', '.join(providers)}")

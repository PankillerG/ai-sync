import argparse

from ai_sync import actions
from ai_sync.commands import utils
from ai_sync.entities import EntityType
from ai_sync.workspace import Workspace


def run(args: argparse.Namespace) -> None:
    work_dir = utils.resolve_work_dir(args.dir)
    scope = utils.get_scope(work_dir)
    ws = Workspace(root=utils.get_workspace_root(work_dir, scope))
    target_dir = actions.init(ws, EntityType(args.entity_type), args.entity_name)

    print(f"Created {args.entity_type} '{args.entity_name}' at {target_dir}/")
    for f in sorted(target_dir.rglob("*")):
        if f.is_file():
            print(f"  {f.relative_to(target_dir)}")

import argparse

from ai_sync import actions
from ai_sync.entities import EntityType
from ai_sync.workspace import Workspace


def run(args: argparse.Namespace) -> None:
    ws = Workspace(root=args.dir)
    target_dir = actions.init(ws, EntityType(args.entity_type), args.entity_name)

    print(f"Created {args.entity_type} '{args.entity_name}' at {target_dir}/")
    for f in sorted(target_dir.rglob("*")):
        if f.is_file():
            print(f"  {f.relative_to(target_dir)}")

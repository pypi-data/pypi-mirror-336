import argparse

from migropy import current_version
from migropy.commands import (
    init_command,
    generate_command,
    upgrade_command,
    downgrade_command,
    list_commands
)

INIT_COMMAND = "init"
GENERATE_COMMAND = "generate"
UPGRADE_COMMAND = "upgrade"
DOWNGRADE_COMMAND = "downgrade"
LIST_REVISIONS_COMMAND = "list"


def main():
    parser = argparse.ArgumentParser(prog="migropy", description="A tool for database migrations")
    subparsers = parser.add_subparsers(dest="command")

    # Init command
    subparsers.add_parser("init", help="project initialization")

    # Generate command
    generate_parser = subparsers.add_parser("generate", help="generate a new migration")
    generate_parser.add_argument("name", type=str, help="migration name")

    # Upgrade command
    subparsers.add_parser("upgrade", help="execute all pending migrations")

    # Downgrade command
    subparsers.add_parser("downgrade", help="execute all pending migrations")

    # List command
    subparsers.add_parser("list", help="list all migrations")

    # Version command
    parser.add_argument("--version", "-v", action="version", version=current_version)

    args = parser.parse_args()

    if args.command == INIT_COMMAND:
        init_command.init_command()
    elif args.command == GENERATE_COMMAND:
        generate_command.generate_command(args.name)
    elif args.command == UPGRADE_COMMAND:
        upgrade_command.upgrade_command()
    elif args.command == DOWNGRADE_COMMAND:
        downgrade_command.downgrade_command()
    elif args.command == LIST_REVISIONS_COMMAND:
        list_commands.list_command()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

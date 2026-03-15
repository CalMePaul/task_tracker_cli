import argparse


def build_parser():
    """Function to build the parser (that accepts commands)."""
    parser = argparse.ArgumentParser(prog="task-tracker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Task description")

    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("task_id", type=int, help="Task ID")
    update_parser.add_argument("description", help="New task description")

    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_id", type=int, help="Task ID")

    mark_parser = subparsers.add_parser("mark", help="Mark task status")
    mark_parser.add_argument("task_id", type=int, help="Task ID")
    mark_parser.add_argument(
        "status",
        choices=["todo", "in-progress", "done"],
        help="New task status",
    )

    return parser


def main():
    """Function that transfers the CLI input to the logic file."""
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "add":
        print(f"add: {args.description}")
    elif args.command == "update":
        print(f"update {args.task_id}: {args.description}")
    elif args.command == "delete":
        print(f"delete {args.task_id}")
    elif args.command == "mark":
        print(f"mark {args.task_id} as {args.status}")


if __name__ == "__main__":
    main()

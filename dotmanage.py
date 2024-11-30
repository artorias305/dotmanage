import os
import shutil
import json
import argparse
from pathlib import Path


CONFIG_FILE = "config.json"
BACKUP_DIR = "backups"


os.makedirs(BACKUP_DIR, exist_ok=True)


def load_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump({}, f)
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)


def backup(app_name):
    config = load_config()
    if app_name not in config:
        print(f"App '{app_name}' not found in config.")
        return

    dotfiles = config[app_name]
    for dotfile in dotfiles:
        source = Path(dotfile).expanduser()
        if not source.exists():
            print(f"Dotfile '{dotfile}' does not exist.")
            continue

        dest = Path(BACKUP_DIR) / app_name / source.name
        try:
            if source.is_dir():
                shutil.copytree(source, dest, dirs_exist_ok=True)
                print(f"Backed up directory '{source}' to '{dest}'.")
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, dest)
                print(f"Backed up file '{source}' to '{dest}'.")
        except PermissionError:
            print(
                f"Permission denied: Unable to back up '{source}'. Please check your permissions."
            )
        except Exception as e:
            print(f"Error: Unable to back up '{source}'. {e}")


def restore(app_name):
    config = load_config()
    if app_name not in config:
        print(f"App '{app_name}' not found in config.")
        return

    dotfiles = config[app_name]
    for dotfile in dotfiles:
        original_path = Path(dotfile).expanduser()
        backup_path = Path(BACKUP_DIR) / app_name / Path(dotfile).name

        if not backup_path.exists():
            print(f"Backup file '{backup_path}' does not exist. Skipping.")
            continue

        try:
            original_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(backup_path, original_path)
            print(f"Restored '{backup_path}' to '{original_path}'.")
        except PermissionError:
            print(
                f"Permission denied: Unable to restore '{backup_path}' to '{original_path}'."
            )
        except Exception as e:
            print(f"Error: Unable to restore '{backup_path}' to '{original_path}'. {e}")


def list_backups():
    backup_path = Path(BACKUP_DIR)
    if not backup_path.exists():
        print("No backups found.")
        return

    for app_folder in backup_path.iterdir():
        if app_folder.is_dir():
            print(f"\nApp: {app_folder.name}")
            for file in app_folder.iterdir():
                print(f" - {file.name}")


def add_to_config(app_name, dotfile):
    config = load_config()
    if app_name not in config:
        config[app_name] = []

    config[app_name].append(dotfile)
    save_config(config)
    print(f"Added dotfile '{dotfile}' for app '{app_name}'.")


def remove_backup(app_name):
    backup_path = Path(BACKUP_DIR) / app_name
    if backup_path.exists():
        shutil.rmtree(backup_path)
        print(f"Removed backups for app '{app_name}'.")
    else:
        print(f"No backups found for app '{app_name}'.")


def main():
    parser = argparse.ArgumentParser(description="Dotfiles Manager")
    subparsers = parser.add_subparsers(dest="command")

    backup_parser = subparsers.add_parser("backup", help="Backup dotfiles for an app")
    backup_parser.add_argument("app_name", help="Name of the app")

    restore_parser = subparsers.add_parser(
        "restore", help="Restore dotfiles for an app"
    )
    restore_parser.add_argument("app_name", help="Name of the app")

    subparsers.add_parser("list", help="List all backups")

    add_parser = subparsers.add_parser("add", help="Add a dotfile to the config")
    add_parser.add_argument("app_name", help="Name of the app")
    add_parser.add_argument("dotfile", help="Path to the dotfile")

    remove_parser = subparsers.add_parser("remove", help="Remove backups for an app")
    remove_parser.add_argument("app_name", help="Name of the app")

    args = parser.parse_args()

    if args.command == "backup":
        backup(args.app_name)
    elif args.command == "restore":
        restore(args.app_name)
    elif args.command == "list":
        list_backups()
    elif args.command == "add":
        add_to_config(args.app_name, args.dotfile)
    elif args.command == "remove":
        remove_backup(args.app_name)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

# Dotfiles Manager

A simple CLI tool to manage, back up, and restore dotfiles for specific applications. This tool helps you keep your configuration files safe and organized, making it easier to migrate or restore your environment.

---

## Features

- **Backup**: Save dotfiles to a centralized `backups/` directory.
- **Restore**: Restore dotfiles to their original locations.
- **List**: View all existing backups.
- **Config Management**: Add or remove dotfiles associated with applications.
- **Cross-platform**: Works on Windows, macOS, and Linux.

---

## Installation

### Prerequisites

- Python 3.6 or later

### Clone the Repository

```bash
git clone https://github.com/artorias305/dotmanage.git
cd dotmanage
```

## Usage

Run the script using Python:

```bash
python dotmanage.py <command> [arguments]
```

### Commands

1. **Add a Dotfile to the Configuration**

Register a dotfile to associate it with an application.

```bash
python dotmanage.py add <app_name> <dotfile_path>
```

2. **Backup Dotfiles**

Backup all dotfiles associated with an application.

```bash
python dotmanage.py backup <app_name>
```

3. **Restore Dotfiles**

Restore all dotfiles for an application to their original locations.

```bash
python dotmanage.py restore <app_name>
```

4. **List Backups**

Display all backed-up dotfiles.

```bash
python dotmanage.py list
```

5. **Remove Backups**

Delete all backups for an application.

```bash
python dotmanage.py remove <app_name>
```

## Configuration File

The configuration file (`config.json`) stores mappings between applications and their dotfiles. It is automatically created and updated by the tool.

### Example `config.json`

```json
{
  "neovim": [".config/nvim"],
  "zsh": ["~/.zshrc", "~/.zsh_aliases"]
}
```

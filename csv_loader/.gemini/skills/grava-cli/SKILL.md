---
name: grava-cli
description: Use when you need to interact with the Grava distributed issue tracker built on Dolt. Triggers on requests to create, manage, list, or update issues, tasks, bugs, or track work progress using the `grava` command.
---

# Grava CLI Skill

Grava is a distributed issue tracker built on top of Dolt. It allows you to manage issues, tasks, and bugs directly from the terminal, leveraging a version-controlled database.

## General Usage

Always use the `grava` command to interact with the tracker. Many commands output human-readable formats but can also accept the `--json` flag for machine-readable output if you need to parse the response.

```bash
grava [command] [flags]
```

## Key Commands and Workflows

### Issue Creation and Management
* **Create an issue:** `grava create` - Creates a new issue.
* **Quickly create an issue:** `grava quick` - Creates an issue quickly with default settings.
* **Create a subtask:** `grava subtask` - Create a subtask under a parent issue.
* **Update an issue:** `grava update` - Modify details of an existing issue.
* **Assign an issue:** `grava assign` - Assign or unassign an issue to/from an actor.
* **Add comments:** `grava comment` - Append a comment to a specific issue.
* **Labeling:** `grava label` - Add or remove labels.

### Status and Progress Tracking
* **List issues:** `grava list` - List all issues.
* **Search issues:** `grava search <query>` - Find issues matching text.
* **Show details:** `grava show` - Display details for a specific issue.
* **Start work:** `grava start` - Mark an issue as started (you are working on it).
* **Stop work:** `grava stop` - Mark an issue as stopped.
* **Claim:** `grava claim` - Claim an issue (sets status to `in_progress`).

### Dependency Management
* **Manage dependencies:** `grava dep` - Link tasks together.
* **View Ready tasks:** `grava ready` - Show tasks that have no unresolved blockers and are ready to be worked on.
* **View Blocked tasks:** `grava blocked` - Show tasks that are currently blocked by other issues.

### Database and Maintenance Operations
* **Start/Stop Server:** `grava db-start` / `grava db-stop` - Controls the underlying Dolt SQL server.
* **Commit changes:** `grava commit` - Commit current changes to the Dolt database.
* **Undo changes:** `grava undo` - Revert the last change to an issue.
* **Archive/Delete:** `grava drop` - Archive an issue or delete all data.
* **Purge old records:** `grava clear` or `grava compact`.
* **System health:** `grava doctor` - Diagnose system health.

## Best Practices
1. **Understand Task State:** Before assigning or working on tasks, consider using `grava ready` or `grava blocked` to understand what is actionable.
2. **Context:** If you need to see the history of an issue, use `grava history`.
3. **Machine Readable:** Add the `--json` flag if you need to programmatically extract an ID or status.
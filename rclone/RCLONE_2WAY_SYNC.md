# 2-Way Synchronization (Bisync)

Rclone's `bisync` command allows you to keep two folders (Cloud and Local) in sync, so changes on either side are reflected on the other.

## 1. Initial Setup (The "Resync")
Before you can start normal 2-way syncing, you must establish a baseline. This tells rclone that both sides are currently identical (or which one is the master).

**Run this command once:**
```bash
rclone bisync "gdrive:FolderName" . --config ./rclone.conf --resync --progress
```

## 2. Regular 2-Way Sync
Once the resync is done, you can run the regular command to merge changes from both sides:
```bash
rclone bisync "gdrive:FolderName" . --config ./rclone.conf --progress
```

## Important Safety Flags
- **Dry Run**: See what would happen without making changes.
  `--dry-run`
- **Conflict Handling**: By default, bisync will rename conflicting files. You can check the logs for notices.
- **Ignore Errors**: If you get minor errors, you can use `--ignore-errors`, but use it with caution.

## Automated Syncing
If you want to automate this, you can create a simple loop or a cron job. 
Example bash loop:
```bash
while true; do
  rclone bisync "gdrive:FolderName" . --config ./rclone.conf --progress
  echo "Sync complete. Waiting 5 minutes..."
  sleep 300
done
```

> [!WARNING]
> Always check the output of the first few runs to ensure it is behaving as expected. `bisync` is more complex than a standard 1-way sync!

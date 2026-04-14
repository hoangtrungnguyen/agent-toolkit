# Rclone Setup Overview

This folder is designated for syncing with your Google Drive using rclone. To get started, you need to complete two main phases:

1.  **[GCP Setup](GCP_SETUP.md)**: Create your own Google Drive Client ID and Secret in the Google Cloud Console.
2.  **[Rclone Configuration](RCLONE_CONFIG.md)**: Configure the rclone CLI to use those credentials.

## Quick Start Configuration
If you have your Client ID and Secret ready, run:
```bash
rclone config --config ./rclone.conf
```

## Useful Commands
- **Sync from Cloud to Local**:
  ```bash
  rclone sync gdrive:/ . --progress
  ```
- **Sync from Local to Cloud**:
  ```bash
  rclone sync . gdrive:/ --progress
  ```

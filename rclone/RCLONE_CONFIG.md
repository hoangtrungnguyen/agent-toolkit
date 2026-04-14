# Rclone CLI Configuration

Once you have your **Client ID** and **Client Secret**, you can configure rclone.

## Phase 1: Initial Configuration
Run this command in this folder:
```bash
rclone config --config ./rclone.conf
```

Follow the interactive prompts:
1.  **n) New remote**: `n`
2.  **name**: `gdrive`
3.  **Storage type**: `drive` (or enter the number for Google Drive)
4.  **client_id**: [Paste your Client ID]
5.  **client_secret**: [Paste your Client Secret]
6.  **scope**: `1` (Full access to all files)
7.  **service_account_file**: [Leave Blank]
8.  **Edit advanced config**: `n`
9.  **Use auto config**: `y` (Your browser will open for authentication)
10. **Configure this as a Shared Drive**: `n`
11. **Keep this remote**: `y` (Yes)
12. **Quit config**: `q`

## Phase 2: Testing the Connection
Run this to see the files on your Google Drive:
```bash
rclone ls gdrive: --config ./rclone.conf
```

## Phase 3: Syncing
To download everything from your drive into this project folder:
```bash
rclone sync gdrive:/ . --config ./rclone.conf --progress
```

> [!WARNING]
> The `sync` command makes the destination *exactly* match the source. 
> Files on the destination that don't exist on the source will be **deleted**. 
> Use `rclone copy` instead if you want to keep local-only files.

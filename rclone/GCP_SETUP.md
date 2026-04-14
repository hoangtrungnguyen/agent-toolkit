# Google Cloud Platform Setup for Rclone

Follow these steps to create your own Client ID and Client Secret for Google Drive access.

## Project Details
- **Project ID**: `rclone-setup-12345` (Already created)
- **API Enabled**: `Google Drive API` (Already enabled)

## Step 1: Configure OAuth Consent Screen
1.  Go to the [OAuth Consent Screen](https://console.cloud.google.com/apis/credentials/consent?project=rclone-setup-12345).
2.  Select **External**, then click **Create**.
3.  **App Information**:
    - **App name**: `rclone`
    - **User support email**: [Select your email]
    - **Developer contact info**: [Your email]
4.  Click **Save and Continue**.

## Step 2: Add Scopes
1.  On the **Scopes** page, click **Add or Remove Scopes**.
2.  Manually add the following scopes in the text box:
    - `https://www.googleapis.com/auth/docs`
    - `https://www.googleapis.com/auth/drive`
    - `https://www.googleapis.com/auth/drive.metadata.readonly`
3.  Click **Add to Table**, then **Update**, then **Save and Continue**.

## Step 3: Add Test User
1.  On the **Test users** page, click **+ Add Users**.
2.  Enter **your Google email address**.
3.  Click **Add**, then **Save and Continue**.

## Step 4: Create Credentials
1.  Go to the [Credentials Page](https://console.cloud.google.com/apis/credentials?project=rclone-setup-12345).
2.  Click **+ Create Credentials** > **OAuth client ID**.
3.  **Application type**: Select `Desktop app`.
4.  **Name**: `rclone` (default is fine).
5.  Click **Create**.
6.  **Copy the Client ID and Client Secret** and keep them safe!

## Step 5: (Optional but Recommended) Publish App
Go back to the **OAuth consent screen** and click **Publish App**. This prevents the credentials from expiring after 7 days if the app is in "Testing" mode.

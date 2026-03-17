# GitHub repo and SSH setup

Follow these steps once to create the repo and use SSH with GitHub.

## 1. Install Git (if needed)

If `git` is not recognized in your terminal:

- Download and install from [git-scm.com](https://git-scm.com/download/win).
- Restart your terminal (and Cursor) after installing.

## 2. Create the GitHub repository

1. Go to [github.com](https://github.com) and sign in.
2. Click the **+** (top right) → **New repository**.
3. Set **Repository name** (e.g. `CloudNativeAI` or `labs`).
4. Choose **Public**, leave "Add a README" **unchecked** (you already have one locally).
5. Click **Create repository**.
6. On the new repo page, note the **SSH** URL, e.g. `git@github.com:YOUR_USERNAME/CloudNativeAI.git`. You’ll use it in step 6.

## 3. Generate an SSH key (one-time per machine)

In **PowerShell**:

```powershell
ssh-keygen -t ed25519 -C "your_email@example.com"
```

- When asked for a file path, press **Enter** to use the default (`C:\Users\coleb\.ssh\id_ed25519`).
- Optionally set a passphrase, or press **Enter** twice for none.

## 4. Add the SSH key to GitHub

1. Copy your **public** key to the clipboard:

   ```powershell
   Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub | Set-Clipboard
   ```

2. On GitHub: **Settings** (your profile menu) → **SSH and GPG keys** → **New SSH key**.
3. Give it a title (e.g. "My PC"), paste the key, then **Add SSH key**.

## 5. Test SSH to GitHub

```powershell
ssh -T git@github.com
```

You should see: `Hi USERNAME! You've successfully authenticated...`

## 6. Initialize the local repo and push

In PowerShell, from this project folder:

```powershell
cd c:\Users\coleb\CloudNativeAI

git init
git add .
git commit -m "Initial commit: OpenRouter lab and devtools"
git branch -M main
git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your GitHub username and the repo name you chose in step 2.

---

Done. Later you can just `git add`, `git commit`, and `git push` as usual.

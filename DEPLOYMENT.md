# Deployment Guide for RA-Rec Demo

## 📋 Quick Summary

Your repository is now ready! Here's what I've set up:

✅ Git repository initialized  
✅ All files committed  
✅ README.md with project information  
✅ .gitignore for Python/Streamlit  
✅ Streamlit configuration  

## 🚀 Step 1: Push to GitHub

### Create a new repository on GitHub

1. Go to [GitHub](https://github.com) and sign in
2. Click the **+** icon in the top right and select **New repository**
3. Name it `demo_UIs` (or your preferred name)
4. **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click **Create repository**

### Push your local repository

Once you create the repo, run these commands in your terminal:

```bash
cd /Users/justincui/Documents/research/demo_UIs

# Add the GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/demo_UIs.git

# Push to GitHub
git push -u origin main
```

If you use SSH keys, use this instead:
```bash
git remote add origin git@github.com:YOUR_USERNAME/demo_UIs.git
git push -u origin main
```

## 🌐 Step 2: Deploy to Streamlit Cloud (Recommended)

**Streamlit Cloud is FREE and perfect for Streamlit apps!**

### Prerequisites
- GitHub account (you just created the repo)
- Your repository must be public (or you need a paid Streamlit plan for private repos)

### Deployment Steps

1. Go to [share.streamlit.io](https://share.streamlit.io)

2. Click **Sign in with GitHub** and authorize Streamlit

3. Click **New app**

4. Fill in the deployment settings:
   - **Repository:** `YOUR_USERNAME/demo_UIs`
   - **Branch:** `main`
   - **Main file path:** `llm_convrec_viz/app.py`

5. Click **Deploy!**

6. Wait 2-3 minutes for deployment (you'll see a build log)

7. Your app will be live at: `https://YOUR_USERNAME-demo-uis.streamlit.app`

### Update README with Live URL

Once deployed, update the README.md file:

```markdown
🚀 [View Live Demo](https://your-app-url.streamlit.app)
```

Then commit and push:
```bash
git add README.md
git commit -m "Add live demo URL"
git push
```

## 🔄 Making Updates

After initial deployment, any updates are automatic:

```bash
# Make changes to your code
git add .
git commit -m "Description of changes"
git push
```

Streamlit Cloud will automatically detect the push and redeploy!

## 🛠️ Alternative Deployment Options

### Option 2: Deploy to Heroku

1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli

2. Create a `Procfile` in the root:
   ```
   web: sh setup.sh && streamlit run llm_convrec_viz/app.py
   ```

3. Create `setup.sh`:
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   \n\
   " > ~/.streamlit/config.toml
   ```

4. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Option 3: Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Click **Start a New Project**
3. Select **Deploy from GitHub repo**
4. Choose your `demo_UIs` repository
5. Railway will auto-detect Streamlit and deploy

### Option 4: Deploy to Google Cloud Run

1. Install gcloud CLI
2. Build and deploy:
   ```bash
   gcloud run deploy rarec-demo \
     --source . \
     --region us-central1 \
     --allow-unauthenticated
   ```

## 🧪 Test Locally Before Deployment

Always test locally first:

```bash
cd /Users/justincui/Documents/research/demo_UIs/llm_convrec_viz
streamlit run app.py
```

Open http://localhost:8501 in your browser to verify everything works.

## 📝 Troubleshooting

### Issue: "Module not found" error
- Make sure `requirements.txt` lists all dependencies
- Update versions if needed

### Issue: App won't start on Streamlit Cloud
- Check the deployment logs for specific errors
- Verify the main file path is correct: `llm_convrec_viz/app.py`
- Ensure requirements.txt is properly formatted

### Issue: Git push fails
- Make sure you've created the remote repository on GitHub first
- Check that you've replaced `YOUR_USERNAME` with your actual GitHub username
- Verify you're authenticated (run `git config --list` to check)

## 🎉 You're All Set!

Your repository structure:
```
demo_UIs/
├── .git/
├── .gitignore
├── .streamlit/
│   └── config.toml
├── README.md
├── DEPLOYMENT.md (this file)
└── llm_convrec_viz/
    ├── app.py
    └── requirements.txt
```

Next steps:
1. ✅ Push to GitHub
2. ✅ Deploy to Streamlit Cloud
3. ✅ Share your demo with the world!

Questions? Check:
- [Streamlit Deployment Docs](https://docs.streamlit.io/streamlit-community-cloud/get-started)
- [GitHub Docs](https://docs.github.com)


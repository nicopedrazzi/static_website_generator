# Static Site Generator

This repo contains a simple static site generator written in Python. It takes Markdown files from `content/` and turns them into a complete HTML site in `docs/`.

## Requirements

- Python 3.10+   
- Git

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### 2. Create and activate a virtual environment (optional, but nice)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Run the generator for local testing

```bash
python3 src/main.py
```

This will read Markdown from `content/` and build the site into `docs/`.

### 4. Open the site locally

You can use any static file server. For example:

```bash
python3 -m http.server --directory docs 8888
```

Then visit:  
http://localhost:8888/

## Deploying With GitHub Pages

1. Push this repo to GitHub (make sure it’s public).
2. Make sure `docs/` is committed (it’s where the HTML gets built).
3. In your GitHub repo:
   - Go to **Settings → Pages**
   - Set **Source** to `main` branch and `/docs` folder

After a minute or two, your site should be live at:

```
https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/
```

## Customizing Content

- Add or edit Markdown files under `content/`
- Keep the same folder structure (e.g. `content/blog/post-name/index.md`)

Re-run:

```bash
python3 src/main.py
```

to regenerate the site.


*** This generator will be updated slowly over time, keep posted for more features!¨***

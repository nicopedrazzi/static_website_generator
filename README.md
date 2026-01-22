# Static Site Generator 

This repo contains a simple static site generator written in Python. It takes Markdown content from the `content/` directory, combines it with a shared HTML template, copies static assets, and outputs a complete static website.

You can use it to generate your own site by editing the content and running the build scripts.

---

## Features

- Markdown → HTML conversion  
- Shared HTML template (`template.html`)  
- Automatic navigation between pages  
- Static asset copying (`static/` → `docs/`)  
- GitHub Pages–ready output in `docs/`  
- Support for a configurable base path (needed for GitHub Pages)  

---

## Requirements

- `python3` (3.9+ recommended)  
- `git`  
- A Unix-like shell (macOS/Linux; Windows users can use WSL or Git Bash)  

---


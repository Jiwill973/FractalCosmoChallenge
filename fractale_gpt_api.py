from fastapi import FastAPI
from fastapi.responses import FileResponse
import httpx
import os
import base64
from pydantic import BaseModel

app = FastAPI(title="FractaleGPT API", version="1.0.0", description="API fractale pour GitHub et la MDF")

# Page d'accueil (ping API)
@app.get("/")
async def root():
    return {"message": "FractalGPT API is alive!"}

# MDF Principles (spirale fractale)
mdf_principles = [
    {"principle": "Transcendental Etymology, Gravitational Pulsation", "expression": "G(t) = G_0 (1 - \\alpha H_0 t)...", "subspiral": "\\kappa_6(z)"},
    {"principle": "Dialectical Fractality, Fractal Expansion", "expression": "H_0(r) = 67.4 + 5.6 e^{-r/147}...", "subspiral": "\\kappa_1(z)"},
    # ... (raccourci pour clarté)
]

@app.get("/mdf-principles")
def get_mdf_principles():
    return {"principles": mdf_principles}

# GitHub: Lister fichiers d'un repo
@app.get("/github/repo/files")
async def get_repo_files(owner: str, repo: str):
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        return {"error": "GitHub token not set"}

    headers = {"Authorization": f"Bearer {github_token}", "Accept": "application/vnd.github+json"}
    async with httpx.AsyncClient() as client:
        url = f"https://api.github.com/repos/{owner}/{repo}/contents"
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

# GitHub: Lire un fichier
@app.get("/github/file/read")
async def read_repo_file(owner: str, repo: str, path: str):
    github_token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"Bearer {github_token}", "Accept": "application/vnd.github+json"}
    async with httpx.AsyncClient() as client:
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        content = base64.b64decode(data["content"]).decode("utf-8")
        return {"path": path, "content": content}

# GitHub: Écrire un fichier
class FileWriteRequest(BaseModel):
    owner: str
    repo: str
    path: str
    content: str
    message: str = "Update file via FractaleGPT API"

@app.post("/github/file/write")
async def write_repo_file(request: FileWriteRequest):
    github_token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"Bearer {github_token}", "Accept": "application/vnd.github+json"}
    async with httpx.AsyncClient() as client:
        url = f"https://api.github.com/repos/{request.owner}/{request.repo}/contents/{request.path}"
        response = await client.get(url, headers=headers)
        sha = response.json().get("sha") if response.status_code == 200 else None

        data = {
            "message": request.message,
            "content": base64.b64encode(request.content.encode("utf-8")).decode("utf-8"),
            "branch": "main"
        }
        if sha:
            data["sha"] = sha

        response = await client.put(url, headers=headers, json=data)
        response.raise_for_status()
        return {"message": f"File {request.path} written successfully"}

# GitHub: Créer une issue
class IssueCreateRequest(BaseModel):
    owner: str
    repo: str
    title: str
    body: str

@app.post("/github/issue/create")
async def create_issue(request: IssueCreateRequest):
    github_token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"Bearer {github_token}", "Accept": "application/vnd.github+json"}
    async with httpx.AsyncClient() as client:
        url = f"https://api.github.com/repos/{request.owner}/{request.repo}/issues"
        data = {"title": request.title, "body": request.body}
        response = await client.post(url, headers=headers, json=data)
        response.raise_for_status()
        return {"message": f"Issue created: {request.title}"}

# Servir le YAML OpenAPI
@app.get("/openapi.yaml")
async def get_openapi_yaml():
    return FileResponse("openapi.yaml")

# Lancement (Render/Local)
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("fractale_gpt_api:app", host="0.0.0.0", port=port, reload=True)

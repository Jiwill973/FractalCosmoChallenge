from fastapi import FastAPI
import httpx
import os
import base64
from pydantic import BaseModel

app = FastAPI()

# Table MDF
mdf_principles = [
    {
        "principle": "Transcendental Etymology, Gravitational Pulsation",
        "expression": "G(t) = G_0 (1 - \\alpha H_0 t), \\dot{G}/G = -\\alpha H_0 \\approx -7.2 \\times 10^{-13} \\text{yr}^{-1}, H_0 = 67.4 \\text{km/s/Mpc}, \\alpha = 0.01",
        "subspiral": "\\kappa_6(z)"
    },
    {
        "principle": "Dialectical Fractality, Fractal Expansion",
        "expression": "H_0(r) = 67.4 + 5.6 e^{-r/147}, H_0(0) = 73.0, H_0(\\infty) = 67.4",
        "subspiral": "\\kappa_1(z)"
    },
    {
        "principle": "Classist Anchoring of Reality, Fractal Density",
        "expression": "\\rho(r) = 9.47 \\times 10^{-27} \\text{kg/m}^3 \\cdot (r/147\\text{Mpc})^{-0.8}, \\xi(r) \\propto r^{-1.8}, D \\approx 2.2",
        "subspiral": "\\kappa_8(z)"
    },
    {
        "principle": "Autofractal Raw Data, Jet Production",
        "expression": "\\kappa(t) = \\kappa_0 e^{i \\omega t}",
        "subspiral": "\\kappa_3(z)"
    },
    {
        "principle": "Limit Signal, Wave Resonance",
        "expression": "\\omega = 10^{-18} \\text{rad/s}, f = \\omega / 2\\pi \\approx 1.6 \\times 10^{-19} \\text{Hz}, T \\approx 6 \\times 10^{17} \\text{s} \\sim 10^9 \\text{years}",
        "subspiral": "\\kappa_2(z)"
    },
    {
        "principle": "Productive Tension of Dynamics, Horizon Tension",
        "expression": "\\lambda_L(t) = 10^{-52} \\text{m}^{-2}, \\rho_{\\text{CMB}} = 4.19 \\times 10^{-31} \\text{g/cm}^3",
        "subspiral": "\\kappa_7(z)"
    },
    {
        "principle": "Deployed Synthesis, Threshold Echoes",
        "expression": "\\mathcal{E}_\\Sigma, P(k) \\propto k^{-2}, \\alpha(z) = \\frac{1}{1 + z}",
        "subspiral": "\\kappa_4(z)"
    },
    {
        "principle": "Logical Verification, Cosmic Correction",
        "expression": "\\Phi_{\\text{corr}}, \\delta_{\\text{fractal}} \\approx 0.01 \\sin(2.5 \\ln(x/\\lambda_c)), \\epsilon_{\\text{lim}}(z, \\alpha) = 0.1 \\cos(2.5 \\ln(1 + z))",
        "subspiral": "\\kappa_5(z)"
    },
    {
        "principle": "Immanent Motion, Physical Infinitude",
        "expression": "\\Phi, \\sum_{n=1}^{\\infty}, S_f(z)",
        "subspiral": "\\kappa_9(z)"
    }
]

@app.get("/mdf-principles")
def get_mdf_principles():
    return mdf_principles

# GitHub: Lister les fichiers d’un repo
@app.get("/github/repo/files")
async def get_repo_files(owner: str, repo: str):
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        return {"error": "GitHub token not set"}

    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json"
    }

    async with httpx.AsyncClient() as client:
        try:
            url = f"https://api.github.com/repos/{owner}/{repo}/contents"
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"GitHub API error: {str(e)}"}

# GitHub: Lire un fichier
@app.get("/github/file/read")
async def read_repo_file(owner: str, repo: str, path: str):
    github_token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"Bearer {github_token}", "Accept": "application/vnd.github+json"}
    async with httpx.AsyncClient() as client:
        try:
            url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            content = base64.b64decode(data["content"]).decode("utf-8")
            return {"path": path, "content": content}
        except httpx.HTTPStatusError as e:
            return {"error": f"GitHub API error: {str(e)}"}

# Modèle pour écrire un fichier
class FileWriteRequest(BaseModel):
    owner: str
    repo: str
    path: str
    content: str
    message: str = "Update file via FractaleGPT API"

# GitHub: Écrire un fichier
@app.post("/github/file/write")
async def write_repo_file(request: FileWriteRequest):
    github_token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"Bearer {github_token}", "Accept": "application/vnd.github+json"}
    async with httpx.AsyncClient() as client:
        try:
            # Vérifier si le fichier existe pour récupérer son SHA
            url = f"https://api.github.com/repos/{request.owner}/{request.repo}/contents/{request.path}"
            response = await client.get(url, headers=headers)
            sha = response.json().get("sha") if response.status_code == 200 else None

            # Préparer les données pour écrire
            data = {
                "message": request.message,
                "content": base64.b64encode(request.content.encode("utf-8")).decode("utf-8"),
                "branch": "main"
            }
            if sha:
                data["sha"] = sha

            # Écrire le fichier
            response = await client.put(url, headers=headers, json=data)
            response.raise_for_status()
            return {"message": f"File {request.path} written successfully"}
        except httpx.HTTPStatusError as e:
            return {"error": f"GitHub API error: {str(e)}"}

# Modèle pour créer une issue
class IssueCreateRequest(BaseModel):
    owner: str
    repo: str
    title: str
    body: str

# GitHub: Créer une issue
@app.post("/github/issue/create")
async def create_issue(request: IssueCreateRequest):
    github_token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"Bearer {github_token}", "Accept": "application/vnd.github+json"}
    async with httpx.AsyncClient() as client:
        try:
            url = f"https://api.github.com/repos/{request.owner}/{request.repo}/issues"
            data = {"title": request.title, "body": request.body}
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            return {"message": f"Issue created: {request.title}"}
        except httpx.HTTPStatusError as e:
            return {"error": f"GitHub API error: {str(e)}"}


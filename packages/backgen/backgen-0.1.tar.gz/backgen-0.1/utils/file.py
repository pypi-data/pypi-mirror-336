import os


def create_project_structure(project_name):
    """Crée la structure d'un projet backend"""
    base_path = f"./{project_name}"

    directories = [
        f"{base_path}/app",
        f"{base_path}/app/routes",
        f"{base_path}/app/models",
        f"{base_path}/app/services",
        f"{base_path}/tests"
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    with open(f"{base_path}/app/main.py", "w") as f:
        f.write(
            """from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get("/")\ndef read_root():\n    return {"message": "Hello, FastAPI!"}\n""")

    print(f"✅ Projet {project_name} créé avec succès.")

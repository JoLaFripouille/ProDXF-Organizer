import cloudconvert
import requests
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis API_KEY.env
load_dotenv('API_KEY.env')

def get_api_key():
    """Récupère la clé API depuis les variables d'environnement."""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("Erreur : Clé API introuvable. Assurez-vous que API_KEY est définie dans API_KEY.env.")
    return api_key

def convert(dwg_file, dxf_file_path):
    """Convertit un fichier DWG en DXF et enregistre le fichier DXF."""
    # Vérifiez que la clé API est bien récupérée
    API_KEY = get_api_key()
    cloudconvert.configure(api_key=API_KEY, sandbox=False)

    # Créer une tâche de conversion avec CloudConvert
    try:
        job = cloudconvert.Job.create(payload={
            "tasks": {
                "import-my-file": {
                    "operation": "import/upload"
                },
                "convert-my-file": {
                    "operation": "convert",
                    "input": "import-my-file",
                    "output_format": "dxf",
                },
                "export-my-file": {
                    "operation": "export/url",
                    "input": "convert-my-file"
                }
            }
        })

        # Obtenir les détails de la tâche d'importation
        upload_task = next(task for task in job['tasks'] if task['name'] == 'import-my-file')
        upload_url = upload_task['result']['form']['url']
        upload_params = upload_task['result']['form']['parameters']

        # Télécharger le fichier DWG sur CloudConvert
        with open(dwg_file, 'rb') as file:
            response = requests.post(upload_url, data=upload_params, files={'file': file})
            response.raise_for_status()

        # Attendre la fin de la conversion et obtenir le lien de téléchargement
        job = cloudconvert.Job.wait(job['id'])
        export_task = next(task for task in job['tasks'] if task['name'] == 'export-my-file')
        file_url = export_task['result']['files'][0]['url']

        # Télécharger le fichier DXF converti
        with requests.get(file_url, stream=True) as r:
            r.raise_for_status()
            with open(dxf_file_path, 'wb') as output_file:
                for chunk in r.iter_content(chunk_size=8192):
                    output_file.write(chunk)

        print(f"Conversion réussie : {dwg_file} -> {dxf_file_path}")

    except Exception as e:
        print(f"Erreur lors de la conversion DWG en DXF : {e}")


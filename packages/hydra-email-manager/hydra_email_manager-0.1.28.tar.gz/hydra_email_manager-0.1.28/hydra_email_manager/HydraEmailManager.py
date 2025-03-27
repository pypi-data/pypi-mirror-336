import os
import requests
from dotenv import load_dotenv

class HydraEmailManager:
    def __init__(self):
        load_dotenv()
        self.api_url = os.getenv("HYDRA_URL")  # URL base da API (ex.: http://localhost:5000)
        self.api_key = os.getenv("HYDRA_API")  # Chave de API para autenticação

        if not self.api_url or not self.api_key:
            raise ValueError("API_URL ou HYDRA_URL não configurados no arquivo .env")

        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }

    def verificar_senha(self, email, password):
        url = f"{self.api_url}/verificar_senha"
        payload = {"email": email, "password": password}
        response = requests.post(url, json=payload, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.json(), "status_code": response.status_code}

    def autenticar(self, email, password):
        url = f"{self.api_url}/autenticar"
        payload = {"email": email, "password": password}
        response = requests.post(url, json=payload, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.json(), "status_code": response.status_code}

    def enviar_email(self, user_email, user_from, subject, body, attachment=None):
        url = f"{self.api_url}/enviar_email"
        payload = {
            "user_email": user_email,
            "user_from": user_from,
            "subject": subject,
            "body": body,
            "attachment": attachment
        }
        response = requests.post(url, json=payload, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.json(), "status_code": response.status_code}

    def baixar_emails(self, user_email, folder_id, is_read=None, file_format="eml", subject_filter=None, from_filter=None, body_filter=None, order_by=None, limit=10, only_attachments=False):
        url = f"{self.api_url}/baixar_emails"
        params = {
            "user_email": user_email,
            "folder_id": folder_id,
            "is_read": is_read,
            "file_format": file_format,
            "subject_filter": subject_filter,
            "from_filter": from_filter,
            "body_filter": body_filter,
            "order_by": order_by,
            "limit": limit,
            "only_attachments": only_attachments
        }
        response = requests.get(url, params=params, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.json(), "status_code": response.status_code}

    def obter_id_pastas(self, user_email, parent_folder_id=None):
        url = f"{self.api_url}/obter_id_pastas"
        params = {"user_email": user_email, "parent_folder_id": parent_folder_id}
        response = requests.get(url, params=params, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.json(), "status_code": response.status_code}

    def limpar_pasta(self, user_email, folder_id):
        url = f"{self.api_url}/limpar_pasta"
        payload = {"user_email": user_email, "folder_id": folder_id}
        response = requests.post(url, json=payload, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.json(), "status_code": response.status_code}
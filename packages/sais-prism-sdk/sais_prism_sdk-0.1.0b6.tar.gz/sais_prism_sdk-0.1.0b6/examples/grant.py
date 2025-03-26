from mlflow.server import get_app_client

# Connect to your MLflow server
tracking_uri = "http://mlflow.internal.sais.com.cn"
auth_client = get_app_client("basic-auth", tracking_uri=tracking_uri)

# Create the users
auth_client.create_user(username="material", password="material_~#")
auth_client.create_user(username="lifescience", password="lifescience_~#")

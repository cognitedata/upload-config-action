import os
import sys
from typing import Tuple

from cognite.experimental import CogniteClient
from cognite.client.exceptions import CogniteAPIKeyError
from cognite.experimental.data_classes.extractionpipelines import ExtractionPipelineConfig


def trim_to_none(st: str) -> str:
    if st is None:
        return st
    st = st.strip()
    if st == "":
        return None
    else:
        return st


def get_client() -> CogniteClient:
    api_key = trim_to_none(os.environ.get("CDF_API_KEY"))
    client_id = trim_to_none(os.environ.get("CDF_CLIENT_ID"))
    client_secret = trim_to_none(os.environ.get("CDF_CLIENT_SECRET"))
    token_url = trim_to_none(os.environ.get("CDF_TOKEN_URL"))
    scopes = trim_to_none(os.environ.get("CDF_SCOPES"))
    audience = trim_to_none(os.environ.get("CDF_AUDIENCE"))
    cdf_project_name = trim_to_none(os.environ.get("CDF_PROJECT_NAME"))
    base_url = trim_to_none(os.environ.get("CDF_BASE_URL", "https://api.cognitedata.com"))
    if not api_key and not audience:
        scopes = scopes.strip().split(" ") if scopes else [f"{base_url}/.default"]

    if (not client_secret or not client_id or not token_url or not cdf_project_name) and not api_key:
        sys.exit("Either OIDC credentials or API key must be specified")

    try:
        if api_key is not None and (
            client_id is not None
            or client_secret is not None
            or token_url is not None
            or scopes is not None
            or audience is not None
        ):
            sys.exit("Please provide only API key configuration or only OAuth2 configuration.")
        elif api_key is not None:
            return CogniteClient(
                client_name="config_upload",
                api_key=api_key,
                base_url=base_url,
                project=cdf_project_name,
                timeout=60,
            )
        else:
            return CogniteClient(
                base_url=base_url,
                client_name="config_upload",
                token_client_id=client_id,
                token_client_secret=client_secret,
                token_url=token_url,
                token_scopes=scopes,
                project=cdf_project_name,
                token_custom_args={"audience": audience} if audience else None,
                timeout=60,
            )
    except CogniteAPIKeyError as e:
        sys.exit(f"Cognite client cannot be initialized: {e}.")


def upload_configs(client: CogniteClient):
    root_folder = os.environ.get("CONFIG_ROOT_FOLDER")
    revision_message = os.environ.get("CONFIG_REVISION_MESSAGE")

    if not root_folder:
        sys.exit("Root folder must be specified")

    config_files: list[Tuple[str, str]] = []

    for root, dirs, files in os.walk(root_folder, followlinks=True):
        for file in files:
            config_files.append((os.path.join(root, file), file))

    print("Uploading config files: ", config_files)

    for file in config_files:
        with open(file[0]) as f:
            result = f.read()

        extid = file[1].rsplit('.', 1)[0]
        print("Uploading config to ", extid)
        config = ExtractionPipelineConfig(
            external_id=extid,
            config=result,
            description=revision_message
        )
        client.extraction_pipelines.new_config(config)


def main() -> None:
    client = get_client()
    deploy = os.environ.get("CONFIG_DEPLOY")
    if deploy and deploy.lower() == "true":
        upload_configs(client)
    else:
        print("CONFIG_DEPLOY is not set to true, configs will not be deployed")

if __name__ == "__main__":
    main()


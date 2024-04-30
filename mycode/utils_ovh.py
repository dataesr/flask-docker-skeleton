import os
import pandas as pd
import swiftclient
import time
import subprocess
from io import BytesIO, TextIOWrapper
from retry import retry

from project.server.main.logger import get_logger

logger = get_logger(__name__)

key = os.getenv('OS_PASSWORD')
project_name = os.getenv('OS_PROJECT_NAME')
project_id = os.getenv('OS_TENANT_ID')
tenant_name = os.getenv('OS_TENANT_NAME')
username = os.getenv('OS_USERNAME')
user = f'{tenant_name}:{username}'
init_cmd = f"swift --os-auth-url https://auth.cloud.ovh.net/v3 --auth-version 3 \
      --key {key}\
      --user {user} \
      --os-user-domain-name Default \
      --os-project-domain-name Default \
      --os-project-id {project_id} \
      --os-project-name {project_name} \
      --os-region-name GRA"

@retry(delay=3, tries=50, backoff=2)
def upload_object_with_destination(container: str, filename: str, destination: str) -> str:
    if destination is None:
        destination = filename.split('/')[-1]
    logger.debug(f'Uploading {filename} in {container} as {destination}')
    cmd = init_cmd + f' upload {container} {filename} --object-name {destination}' \
                     f' --segment-size 1048576000 --segment-threads 100'
    #os.system(cmd)
    r = subprocess.check_output(cmd, shell=True)
    return f'https://storage.gra.cloud.ovh.net/v1/AUTH_{project_id}/{container}/{destination}'

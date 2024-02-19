import requests
import os
import pandas as pd

from project.server.main.logger import get_logger

logger = get_logger(__name__)


def check_cordis(args):
    projects_ids = args.get('projects', [])
    suffix = args.get('suffix')
    logger.debug(f'{len(projects_ids)} projects_ids')
    res = []
    for ix, p in enumerate(projects_ids):
        url = f"https://cordis.europa.eu/project/id/{p}"
        logger.debug(f'{url} ({ix+1}/{len(projects_ids)})')
        request_response = requests.head(url).status_code
        res.append({'project_id': p, 'cordis_webPage_status': request_response})
    df = pd.DataFrame(res)
    os.system('mkdir -p /data/cordis')
    df.to_csv(f'/data/cordis/cordis_{suffix}.csv', index=False)

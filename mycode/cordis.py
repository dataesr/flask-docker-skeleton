import requests
import os
import pandas as pd
from mycode.utils_ovh import upload_object_with_destination
from project.server.main.logger import get_logger

logger = get_logger(__name__)


def check_cordis(args):
    projects_ids = args.get('projects', [])
    suffix = args.get('suffix')
    logger.debug(f'{len(projects_ids)} projects_ids')
    res = []
    output_file = args.get('output_file', 'cordis').split('.')[0]
    for ix, p in enumerate(projects_ids):
        url = f"https://cordis.europa.eu/project/id/{p}"
        logger.debug(f'{url} ({ix+1}/{len(projects_ids)})')
        request_response = requests.head(url).status_code
        res.append({'project_id': p, 'cordis_webPage_status': request_response})
    df = pd.DataFrame(res)
    os.system('mkdir -p /data/cordis')
    new_filename = f'/data/cordis/{output_file}_{suffix}.csv'
    assert('*' not in new_filename)
    assert(' ' not in new_filename)
    os.system('rm  -rf {new_filename}')
    df.to_csv(new_filename, index=False)

def gather_cordis(args):
    all_df = []
    output_file = args.get('output_file', 'cordis').split('.')[0]
    for f in os.listdir('/data/cordis'):
        if output_file in f:
            current_file = f'/data/cordis/{f}'
            all_df.append(pd.read_csv(current_file))
    df = pd.concat(all_df)
    new_filename = f'/data/cordis/{output_file}.csv'
    os.system('rm  -rf {new_filename}')
    df.to_csv(new_filename, index=False)
    upload_object_with_destination('eCorda', new_filename, new_filename)

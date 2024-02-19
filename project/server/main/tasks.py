import sys
import os
from mycode import ff
#from mycode.bso_coverage import bso_coverage
from project.server.main.logger import get_logger

logger = get_logger(__name__)


def create_task_compute(args: dict) -> None:
    logger.debug(f"Creating task with args {args}")
    #error = bso_coverage.test_mother_duck()
    logger.debug(f"Task ended with error {error}")

def create_task_check_cordis(args):
    projects_ids = args.get('projects', [])
    suffix = args.get('suffix')
    logger.debug(f'{len(projects_ids)} projects_ids')
    res = []
    for ix, p in enumerate(projects_ids):
        url = f"https://cordis.europa.eu/project/id/{p}"
        logger.debug(f'{url} ({ix}/{len(projects_ids)}')
        request_response = requests.head(url).status_code
        res.append({'project_id': p, 'cordis_webPage_status': request_response})
    df = pd.DataFrame(res)
    os.system('mkdir -p /data/cordis')
    df.to_csv(f'/data/cordis/cordis_{suffix}.csv', index=False)

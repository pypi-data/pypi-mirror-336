# KatapultAPI

katapultAPI is a Python module designed to handle requests made to the Katapult API.


## Installation & Setup

```bash
pip install katapult-api
```

## Usage

### Getting a Job list and Job Details

```python
import logging.config
import asyncio

# Not required but the client itself has logging functionality to help track requests.
logger = logging.getLogger(__name__)
logging.basicConfig(
        level=logging.DEBUG,
        format='[%(levelname)s] %(asctime)s - %(name)s - %(message)s'
    )

from katapult_api.katapult import Katapult
from katapult_api.utils import task_handler

async def main():

    # Sets up the aiohttp session and closes it after finishing.
    async with Katapult(api_key="YOURAPIKEY") as katapult:

        # Returns a Response object that contains attributes such as return status, content, and even a json() method.
        job_lists = await katapult.job_lists()

        # Here we build 20 payloads that will be sent out at the same time.
        job_ids = [{"job_id":key} for key in list(job_lists.json().keys())[:20]]

        # Not required but makes setting up async tasks easy, pass in a job name and a list of dicts that contain
        # expected params.
        results = await task_handler(katapult.job,job_ids)
    return results

if __name__ == '__main__':
    logger.info(f"Getting jobs...")
    jobs = asyncio.run(main())
    logger.info(f"Finished, got {len(jobs)} jobs.")
```

### Creating a Node
```python
import asyncio

# ...possible logging

from katapult_api.katapult import Katapult

async def main():

    async with Katapult(api_key="YOURAPIKEY") as katapult:

        # get job id from job_lists endpoint...
        job_id = "-ABC123"

        # create a node by passing job id, lat/long, and a flat dict of attributes to write to the node
        results = await katapult.create_node(job_id,30.0817,-97.843,{"OID":123,"my_custom_attr":"howdy partner"})

    return results

if __name__ == '__main__':
    results = asyncio.run(main())
```

### KatapultNice Usage
```python
import logging.config
import asyncio

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

from katapult_api.katapult import Katapult
from katapult_api.katapult_nice import KatapultNice
from katapult_api.utils import task_handler

async def main(api_key: str):
    async with KatapultNice(api_key=api_key) as nice:
        job_lists = await nice.job_lists()
        job_ids = [{"job_id": key} for key in list(job_lists.json().keys())[:20]]
        results = await task_handler(nice.job_nodes, job_ids)
    return results


if __name__ == '__main__':
    api_key = "api_key"
    logger.info(f"Getting jobs...")
    jobs = asyncio.run(main(api_key))
    logger.info(f"Finished, got {len(jobs)} jobs.")

```

## Resources
- https://documenter.getpostman.com/view/9081167/SVtVV93W: Katapultpro API V1
- https://github.com/KatapultDevelopment/katapult-pro-api-documentation?tab=readme-ov-file: Katapultpro Github
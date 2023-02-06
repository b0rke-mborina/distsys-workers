# distsys-workers

**To start master service run its script by using command (in project root folder):**
- python serviceMaster.py

**To start one worker run its script by using command (in project root folder):**
- python workers/serviceWorker1.py
- python workers/serviceWorker2.py
- python workers/serviceWorker3.py
- python workers/serviceWorker4.py
- python workers/serviceWorker5.py
- python workers/serviceWorker6.py
- python workers/serviceWorker7.py
- python workers/serviceWorker8.py
- python workers/serviceWorker9.py
- python workers/serviceWorker10.py

**Send clients' requests to master service for processing run client script by by using command (in project root folder):**
- python client.py

**Commented out features / functionalities:**
- printing max number of tasks possible (when codes of each of the 10 files are sent separately, that is complete client's code isn't divided into equal chunks; serviceMaster.py lines 46 - 49)

**Data in *data/dataset.json*:**  https://huggingface.co/datasets/codeparrot/codeparrot-clean/resolve/main/file-000000000040.json.gz

**Dependencies:**
- asyncio
- aiohttp
- pandas
- random (Python standard library)
- logging (Python standard library)
- re (Python standard library)
- string (Python standard library)
- vyper (Python standard library)

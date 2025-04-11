
import os
import sys

from modules import scripts
sys.path.append(os.path.join(scripts.basedir(), 'scripts'))

import modules.script_callbacks as script_callbacks
from api.interrogate_api import InterrogateApi

try:
    api = InterrogateApi()
    script_callbacks.on_app_started(api.start)
except:
    pass

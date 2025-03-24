import requests

from ..logging.base_logger import APP_LOGGER
from ..interfaces.interfaces_th import NchanPayload_TH
from ..utils.env_initializer import EnvStore
from ..ioc.singleton import SingletonMeta
from .context_utils import ContextUtils


class NchanUtils(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._nchan_url = EnvStore().nchan_domain

    def publish(self, payload: NchanPayload_TH):
        headers = ContextUtils.get_headers_details()
        nchan_url = self._nchan_url + "/pub/" + headers.sessionid
        try:
            response = requests.request(method="POST", url=nchan_url, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            APP_LOGGER.error(f"Failed  to Publish to Nchan : {e}")
            pass

# © Copyright Databand.ai, an IBM Company 2022
import logging

from typing import Optional, Tuple

from airflow_monitor.data_fetcher.plugin_metadata import get_plugin_metadata
from dbnd_monitor.adapter.adapter import Assets, MonitorAdapter, ThirdPartyInfo


logger = logging.getLogger(__name__)


class AirflowAdapter(MonitorAdapter):
    def init_cursor(self) -> str:
        raise NotImplementedError()

    def get_new_assets_for_cursor(self, cursor: str) -> Tuple[Assets, str]:
        raise NotImplementedError()

    def get_assets_data(self, assets: Assets) -> Assets:
        raise NotImplementedError()

    def get_third_party_info(self) -> Optional[ThirdPartyInfo]:
        metadata = get_plugin_metadata()
        metadata_dict = metadata.as_safe_dict() if metadata else {}

        return ThirdPartyInfo(metadata=metadata_dict, error_list=[])

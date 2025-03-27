
import time
import requests
from typing import Iterator

from airbyte_cdk.sources import AbstractSource
from airbyte_cdk.models import SyncMode, ConfiguredAirbyteCatalog, AirbyteMessage, AirbyteRecordMessage, AirbyteStreamStatus
from airbyte_cdk.sources.streams import Stream
from airbyte_cdk.sources.streams.http import HttpStream
from airbyte_cdk.models.airbyte_protocol import Type
from datetime import datetime


class SalesforceBulkQueryStream(Stream):
    def __init__(self, config):
        self.config = config
        self.access_token = config["access_token"]
        self.instance_url = config["instance_url"]
        self.soql_query = config["soql_query"]
        self.api_version = "62.0"

    def get_json_headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def submit_bulk_query(self):
        url = f"{self.config['instance_url']}/services/data/v{self.api_version}/jobs/query"
        body = {
            "operation": "query",
            "query": self.soql_query,
            "contentType": "JSON"
        }
        response = requests.post(url, headers=self.get_json_headers(), json=body)
        response.raise_for_status()
        return response.json()["id"]

    def wait_for_completion(self, job_id):
        status_url = f"{self.config['instance_url']}/services/data/v{self.api_version}/jobs/query/{job_id}"
        while True:
            resp = requests.get(status_url, headers=self.get_json_headers())
            resp.raise_for_status()
            status = resp.json()["state"]
            if status == "JobComplete":
                return
            elif status in ["Aborted", "Failed"]:
                raise Exception(f"Bulk job failed with status: {status}")
            time.sleep(2)

    def download_results(self, job_id):
        url = f"{self.config['instance_url']}/services/data/v{self.api_version}/jobs/query/{job_id}/results"
        headers = self.get_json_headers()
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        for line in response.iter_lines():
            if line:
                yield line

    def read_records(self, sync_mode: SyncMode, cursor_field: list = None, stream_slice: dict = None,
                     stream_state: dict = None) -> Iterator[dict]:
        job_id = self.submit_bulk_query()
        self.wait_for_completion(job_id)
        for line in self.download_results(job_id):
            yield eval(line)

    def get_json_schema(self) -> dict:
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {}
        }

    @property
    def name(self) -> str:
        return "salesforce_bulk_query"

    @property
    def primary_key(self) -> str:
        return None

    def get_cursor_field(self) -> list:
        return []

    def stream_slices(self, **kwargs) -> list:
        return [None]


from airbyte_cdk.sources import AbstractSource
from .source import SalesforceBulkQueryStream


class SourceSalesforceBulk(AbstractSource):
    def check_connection(self, logger, config) -> (bool, any):
        try:
            stream = SalesforceBulkQueryStream(config)
            stream.submit_bulk_query()
            return True, None
        except Exception as e:
            return False, str(e)

    def streams(self, config):
        return [SalesforceBulkQueryStream(config)]

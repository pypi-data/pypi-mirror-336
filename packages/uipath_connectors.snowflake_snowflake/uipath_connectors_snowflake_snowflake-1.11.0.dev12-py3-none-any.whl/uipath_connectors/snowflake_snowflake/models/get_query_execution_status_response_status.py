from enum import Enum


class GetQueryExecutionStatusResponseStatus(str, Enum):
    BLOCKED = "BLOCKED"
    FAILEDWITHERROR = "FAILED_WITH_ERROR"
    FAILEDWITHINCIDENT = "FAILED_WITH_INCIDENT"
    QUEUED = "QUEUED"
    RESUMINGWAREHOUSE = "RESUMING_WAREHOUSE"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"

    def __str__(self) -> str:
        return str(self.value)

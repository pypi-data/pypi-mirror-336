from typing import Optional, TypedDict

from pydantic import BaseModel
from pymediasoup.consumer import Consumer


class RemotePeerEvents(str):
    StreamAvailable = "stream_available"
    StreamPlayable = "stream_playable"
    StreamClosed = "stream_closed"
    StreamPaused = "stream_paused"
    MetaDataUpdated = "metadata_updated"
    RoleUpdated = "role_updated"


class RemotePeerEventsData:
    class StreamAvailable(TypedDict):
        label: str
        producerId: str

    class StreamPlayable(TypedDict):
        label: str
        consumer: Consumer

    class StreamClosed(BaseModel):
        class StreamClosedReason(BaseModel):
            code: int
            tag: str
            message: str

        label: str
        reason: Optional[StreamClosedReason]

    class StreamPaused(TypedDict):
        label: str
        producerId: str
        peerId: str

    class MetaDataUpdated(TypedDict):
        metadata: str

    class RoleUpdated(TypedDict):
        role: Optional[str]

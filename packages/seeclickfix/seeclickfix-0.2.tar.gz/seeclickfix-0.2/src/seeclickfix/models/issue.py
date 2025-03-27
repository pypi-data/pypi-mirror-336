from dataclasses import dataclass
from typing import Optional
from enum import Enum
from datetime import datetime
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Errors:
    pass


@dataclass_json
@dataclass
class Media:
    video_url: None
    representative_image_url: str
    image_full: Optional[str] = None
    image_square_100_x100: Optional[str] = None


class Status(Enum):
    ACKNOWLEDGED = "Acknowledged"
    CLOSED = "Closed"
    OPEN = "Open"


@dataclass_json
@dataclass
class Issue:
    id: int
    status: str
    summary: str
    description: str
    lat: float
    lng: float
    address: str
    created_at: str
    url: str
    media: Media
    rating: Optional[int] = None # Issue endpoint
    acknowledged_at: Optional[str] = None
    closed_at: Optional[str] = None
    reopened_at: Optional[str] = None # Issue endpoint
    shortened_url: Optional[str] = None # Issue endpoint


@dataclass_json
@dataclass
class Pagination:
    entries: int
    page: int
    per_page: int
    pages: int
    next_page: int
    next_page_url: str
    previous_page: Optional[int] = None
    previous_page_url: Optional[str] = None


@dataclass_json
@dataclass
class Metadata:
    pagination: Pagination


@dataclass_json
@dataclass
class RootObject:
    issues: list[Issue]
    metadata: Metadata
    errors: Errors

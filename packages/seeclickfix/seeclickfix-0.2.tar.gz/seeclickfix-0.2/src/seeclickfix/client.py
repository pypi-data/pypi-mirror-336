import logging
import aiohttp
from .adapter import RestAdapter
from .models.issue import RootObject


class SeeClickFixClient:
    """Client for interacting with the SeeClickFix API"""

    def __init__(
        self, session: aiohttp.ClientSession, logger: logging.Logger = None
    ) -> None:
        self._logger = logger or logging.getLogger(__name__)
        self.session = session
        self.adapter = RestAdapter(
            self.session, hostname="seeclickfix.com", base="api/v2"
        )

    async def get_issues(
        self,
        min_lat: float,
        min_lng: float,
        max_lat: float,
        max_lng: float,
        status: str,
        fields: str,
        page: int,
    ) -> RootObject:
        """Get a list of issues"""
        params = {
            "min_lat": min_lat,
            "min_lng": min_lng,
            "max_lat": max_lat,
            "max_lng": max_lng,
            "status": status,
            "fields[issue]": fields,
            "page": page,
        }
        result = await self.adapter.get("issues", ep_params=params)
        return RootObject.from_dict(result.data)

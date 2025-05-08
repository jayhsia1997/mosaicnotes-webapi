"""
Handler for demo-related operations
"""
from app.libs.database import Session
from app.models import Demo
from app.serializers.mixins import GenericQueryBaseModel
from app.serializers.v1.demo import DemoDetail, DemoList, DemoPages


class DemoHandler:
    """DemoHandler"""

    def __init__(
        self,
        session: Session = None,
    ):
        """initialize"""
        self._session = session

    async def get_pages(
        self,
        query_model: GenericQueryBaseModel
    ) -> DemoPages:
        """
        Get demo pages
        :param query_model:
        :return:
        """
        items, total = await (
            self._session.select(
                Demo.id,
                Demo.name,
                Demo.remark
            )
            .limit(query_model.page_size)
            .offset(query_model.page * query_model.page_size)
            .fetchpages(as_model=DemoDetail)
        )
        return DemoPages(
            items=items,
            total=total,
            page=query_model.page,
            page_size=query_model.page_size
        )

    async def get_list(
        self
    ) -> DemoList:
        """
        Get demo list
        :return:
        """
        items = await (
            self._session.select(
                Demo.id,
                Demo.name,
                Demo.remark
            )
            .fetch(as_model=DemoDetail)
        )
        return DemoList(
            items=items
        )

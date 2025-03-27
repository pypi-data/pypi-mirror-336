from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy import and_, or_, desc, asc, func
from typing import Dict, List, Any, Type, Optional
from sqlalchemy.orm import DeclarativeMeta

class QueryBuilder:
    def __init__(
        self, 
        model: Type[DeclarativeMeta], 
        session: AsyncSession,
        filters: Optional[Dict[str, Any]] = None,
        search: Optional[str] = None,
        search_fields: Optional[List[str]] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "asc",
        page: int = 1,
        page_size: int = 10
    ):
        self.model = model
        self.session = session
        self.filters = filters or {}
        self.search = search
        self.search_fields = search_fields or []
        self.sort_by = sort_by
        self.sort_order = sort_order.lower()
        self.page = max(page, 1)
        self.page_size = max(page_size, 1)

    def apply_filters(self, query):
        conditions = []
        for field, value in self.filters.items():
            if hasattr(self.model, field):
                column = getattr(self.model, field)
                if isinstance(value, list):
                    conditions.append(column.in_(value))
                elif isinstance(value, dict):
                    if "gte" in value:
                        conditions.append(column >= value["gte"])
                    if "lte" in value:
                        conditions.append(column <= value["lte"])
                else:
                    conditions.append(column == value)
        if conditions:
            query = query.filter(and_(*conditions))
        return query

    def apply_search(self, query):
        if self.search and self.search_fields:
            search_conditions = []
            for field in self.search_fields:
                if hasattr(self.model, field):
                    column = getattr(self.model, field)
                    if column.type.python_type == str:
                        search_conditions.append(func.to_tsvector('english', column).match(self.search))
            if search_conditions:
                query = query.filter(or_(*search_conditions))
        return query

    def apply_sorting(self, query):
        if self.sort_by and hasattr(self.model, self.sort_by):
            column = getattr(self.model, self.sort_by)
            order = asc(column) if self.sort_order == "asc" else desc(column)
            query = query.order_by(order)
        return query

    def apply_pagination(self, query):
        offset = (self.page - 1) * self.page_size
        query = query.offset(offset).limit(self.page_size)
        return query

    async def execute(self):
        query = select(self.model)
        query = self.apply_filters(query)
        query = self.apply_search(query)
        query = self.apply_sorting(query)
        query = self.apply_pagination(query)
        result = await self.session.execute(query)
        return result.scalars().all()

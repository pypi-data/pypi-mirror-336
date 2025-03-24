"""ORM client for an specific inventory in SciNote."""

import logging

from aiocache import Cache

from .items import Item
from ..client.api.inventory_column_client import InventoryColumnClient
from ..client.api.inventory_item_client import InventoryItemClient
from ..client.models.inventory_cell import CreateInventoryCell

logger = logging.getLogger(__name__)

# How long we cache result from SciNote before refreshing.
CACHE_TIMEOUT_SECONDS = 120


class Inventory:
    """ORM client for a specific inventory in SciNote."""

    def __init__(
        self,
        name: str,
        column_client: InventoryColumnClient,
        item_client: InventoryItemClient,
    ):
        self.column_client = column_client
        self.item_client = item_client
        self.name = name
        self.__columns = {}
        self.__item_list = []
        self.__cache = Cache(Cache.MEMORY, ttl=CACHE_TIMEOUT_SECONDS)

    async def load_columns(self) -> None:
        """Load the columns for this inventory."""

        if not await self.__cache.exists('columns'):
            columns = await self.column_client.get_columns()
            self.__columns = {}
            for column in columns:
                name = column.attributes.name.lower().replace(' ', '_')
                self.__columns[name] = column
            await self.__cache.set('columns', True)

    async def load_items(self) -> None:
        """Load the items for this inventory."""

        if not await self.__cache.exists('items'):
            items = await self.item_client.get_items()
            self.__item_list = []
            for item in items:
                self.__item_list.append(
                    Item(
                        item.id,
                        item.attributes.name,
                        item.attributes.created_at,
                        self.item_client,
                        self.__columns,
                        item.inventory_cells,
                    )
                )
            await self.__cache.set('items', True)

    async def items(self) -> list[Item]:
        """Get the items for this inventory."""
        await self.load_columns()
        await self.load_items()
        return self.__item_list

    async def match(self, **kwargs) -> list[Item]:
        """Return matching items from this inventory."""
        await self.load_columns()
        await self.load_items()
        return [item for item in self.__item_list if item.match(**kwargs)]

    async def columns(self):
        """Get the columns for this inventory."""
        await self.load_columns()
        return [column for column in self.__columns.values()]

    async def has_column(self, name: str) -> bool:
        """Check if the inventory has a column."""
        await self.load_columns()
        return name in self.__columns

    async def create_item(self, name: str, **kwargs) -> Item:
        """Create a new item in this inventory."""
        await self.load_columns()

        cells = []
        for key, value in kwargs.items():
            if key not in self.__columns:
                raise ValueError(f'Column {key} does not exist in inventory.')

            column = self.__columns[key]
            cells.append(CreateInventoryCell(value=value, column_id=column.id))

        item = await self.item_client.create_item(name, cells)

        new_item = Item(
            item.id,
            item.attributes.name,
            item.attributes.created_at,
            self.item_client,
            self.__columns,
            item.inventory_cells,
        )
        self.__item_list.append(new_item)
        return new_item

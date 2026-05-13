"""
Simple in-memory item store with logging and type hints.
Can be replaced by a database adapter without changing the API.
"""
import logging
import uuid
from typing import List, Optional, Dict
from datetime import datetime, timezone
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class Item(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class ItemStore:
    def __init__(self):
        self._items: Dict[str, Item] = {}
        self._seed_demo_data()

    def _seed_demo_data(self):
        """Pre-populate with sample items for demo purposes."""
        demo_names = ["Laptop", "Cloud Server", "API Gateway", "Database Cluster", "Load Balancer"]
        for name in demo_names:
            self.add_item(name)

    def add_item(self, name: str) -> Item:
        if not name.strip():
            raise ValueError("Item name cannot be empty")
        item = Item(name=name.strip())
        self._items[item.id] = item
        logger.info("Item added: id=%s name=%s", item.id, item.name)
        return item

    def get_all(self) -> List[Item]:
        return list(self._items.values())

    def get_by_id(self, item_id: str) -> Optional[Item]:
        return self._items.get(item_id)

    def delete_item(self, item_id: str) -> bool:
        if item_id in self._items:
            del self._items[item_id]
            logger.info("Item deleted: id=%s", item_id)
            return True
        return False

# Global instance (singleton for demo; inject in production)
item_store = ItemStore()
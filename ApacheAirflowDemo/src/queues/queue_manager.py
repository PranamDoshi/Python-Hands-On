"""Queue manager for handling extractor and crawler queues."""
import json
import redis
from typing import Dict, Any, Optional
from datetime import datetime
from src.config.settings import settings
from src.schema.schemas import QueueMessage


class QueueManager:
    """Manages queues for extractor and crawler tasks."""
    
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL)
        self.extractor_queue = settings.EXTRACTOR_QUEUE_NAME
        self.crawler_queue = settings.CRAWLER_QUEUE_NAME
    
    def push_to_extractor_queue(self, crawl_id: str, payload: Dict[str, Any]) -> bool:
        """Push a task to the extractor queue."""
        try:
            message = QueueMessage(
                crawl_id=crawl_id,
                task_id=f"{crawl_id}_{datetime.now().isoformat()}",
                payload=payload
            )
            self.redis_client.lpush(
                self.extractor_queue,
                message.model_dump_json()
            )
            return True
        except Exception as e:
            print(f"Error pushing to extractor queue: {e}")
            return False
    
    def pop_from_extractor_queue(self, timeout: int = 0) -> Optional[QueueMessage]:
        """Pop a task from the extractor queue."""
        try:
            result = self.redis_client.brpop(self.extractor_queue, timeout=timeout)
            if result:
                _, message_json = result
                message_data = json.loads(message_json)
                return QueueMessage(**message_data)
            return None
        except Exception as e:
            print(f"Error popping from extractor queue: {e}")
            return None
    
    def push_to_crawler_queue(self, crawl_id: str, pdp_id: str, pdp_url: str) -> bool:
        """Push a PDP task to the crawler queue."""
        try:
            message = QueueMessage(
                crawl_id=crawl_id,
                task_id=pdp_id,
                payload={"pdp_id": pdp_id, "pdp_url": pdp_url}
            )
            self.redis_client.lpush(
                self.crawler_queue,
                message.model_dump_json()
            )
            return True
        except Exception as e:
            print(f"Error pushing to crawler queue: {e}")
            return False
    
    def pop_from_crawler_queue(self, timeout: int = 0) -> Optional[QueueMessage]:
        """Pop a task from the crawler queue."""
        try:
            result = self.redis_client.brpop(self.crawler_queue, timeout=timeout)
            if result:
                _, message_json = result
                message_data = json.loads(message_json)
                return QueueMessage(**message_data)
            return None
        except Exception as e:
            print(f"Error popping from crawler queue: {e}")
            return None
    
    def get_queue_length(self, queue_name: str) -> int:
        """Get the length of a queue."""
        try:
            return self.redis_client.llen(queue_name)
        except Exception as e:
            print(f"Error getting queue length: {e}")
            return 0

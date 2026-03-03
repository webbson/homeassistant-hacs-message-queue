"""Constants for the Message Queue integration."""

DOMAIN = "message_queue"
STORAGE_KEY = "message_queue.queues"
STORAGE_VERSION = 1
SIGNAL_QUEUE_UPDATED = f"{DOMAIN}_queue_updated"

CONF_ROTATION_INTERVAL = "rotation_interval"
CONF_DEFAULT_SHOW_SECONDS = "default_show_seconds"
CONF_QUEUES = "queues"

DEFAULT_ROTATION_INTERVAL = 5
DEFAULT_SHOW_SECONDS = 3600

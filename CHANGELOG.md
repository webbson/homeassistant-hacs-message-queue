# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-03-03

### Added
- Initial release as HACS custom integration
- Config flow UI for initial setup (rotation interval, default show seconds)
- Options flow for managing queues (add, remove) and editing settings
- Sidebar panel ("Messages") for sending messages without YAML
- Native HA services visible in Developer Tools > Services with field descriptions
- Multiple independent queues with one sensor entity per queue
- Per-message expiration via `show_seconds` or absolute `show_until`
- Batch messaging to single, multiple, or all queues
- Persistence via HA's `.storage/` system
- `message_queue_status` event fired by `get_queue_status` service
- HACS support for easy installation and updates

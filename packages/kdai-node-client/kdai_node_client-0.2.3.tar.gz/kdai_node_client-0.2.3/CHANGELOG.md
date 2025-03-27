# Changelog

All notable changes to kdai-node-client will be documented in this file.

## 0.1.2 (2025-03-27)

### Fixed
- Fixed API request compatibility issues:
  - Updated node registration payload format to match server expectations
  - Added proper `node_token` and `node_info` structure for registration
  - Ensured system information is included in all API requests
  - Maintained consistent payload structure across all API endpoints

## 0.1.1 (2025-03-27)

### Fixed
- Implemented comprehensive HTTP to HTTPS redirect handling:
  - Added `allow_redirects=False` parameter to all HTTP requests
  - Added automatic detection and handling of HTTP/HTTPS redirects
  - Server URL is automatically updated from HTTP to HTTPS when redirected
  - Improved manual tracking of redirects for all API endpoints
- Enhanced error handling with better JSON response validation
- Improved error logging for network connectivity issues

## 0.1.0 (2025-03-25)

### Added
- Initial release of the KDAI Node Client
- Support for node registration and authentication
- WebSocket-based communication with KDAI server
- Task management system
- System information gathering and reporting
- Heartbeat mechanism
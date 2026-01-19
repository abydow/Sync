# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.0.4] - 2026-01-20

### Added

- **Database:**
  - Integrated **Supabase** and **Alembic** for database migrations (`alembic.ini`, `migrations/`).
  - Added test suite for database connections (`test/test_db.py`).
- **Events (New Module):**
  - Added `src/cogs/events/listeners.py` to handle core events.
  - `on_message`: Automatically registers guilds in the database.
  - `on_member_join`: Implemented welcome messages and auto-role assignment.
  - `on_guild_join`: Initializes guild configuration and DMs the server owner.
  - `on_guild_remove` & `on_member_remove`: Added usage logging.

### Changed

- **Refactor:**
  - Moved event handling logic to `src/cogs/events/listeners.py`.

## [0.0.3] - 2026-01-18

### Added

- **Database:**
  - Implemented SQLAlchemy-based database integration.
  - Added `Guild` and `User` models for persistent storage.
  - Created `DatabaseService` for managing guild configurations and user data.
- **Architecture:**
  - Restructured project layout for better scalability.

### Changed

- Refactored `main.py` and cogs for better code quality and linting.
- Improved error handling and minor bug fixes.

## [0.0.2] - 2026-01-10

### Added

- **Basic Commands:**
  - `ping`: Check bot latency.
  - `info`: Display general bot statistics.
  - `userinfo`: Show details about a user.
  - `serverinfo`: Show details about the current server.
- **Legal & Documentation:**
  - Added `PRIVACY_POLICY.md`.
  - Added `TERMS_OF_SERVICE.md`.
- **Development:**
  - Added `requirements-dev.txt`.

## [0.0.1] - 2026-01-09

### Added

- **Initial Project Setup:**
  - Created the core bot structure using `discord.py`.
  - Implemented basic event handling for `on_ready` and `on_guild_join`.
  - Set up environment variable loading using `python-dotenv` for secure token management.
  - Configured basic logging to the console for monitoring bot status.
  - Added project documentation files: `README.md`, `CONTRIBUTING.md`, and `CHANGELOG.md`.
  - Created an initial `.gitignore` file for Python projects.

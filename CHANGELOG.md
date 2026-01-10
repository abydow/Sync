# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

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

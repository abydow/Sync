## 20th dec

- added CONTRIBUTION.md
- License
- README.md
- .gitignore

## 21st Dec

- Added the sqlite package
- created a database table to store the data of user and guild and a integer slot for storing warnings issued.
- created create_user_table() to make the database with primary key of (user_id,guild_id)
- created increase_and_get warnings() function to count warning
  - If the user has no history it will add the user and also update the database with 1 warning
  - If the user is already in the database it will add +1 warning

## 22nd Dec

- Updated the code and removed the "Interesting" reply feature
- Also included the profanity check loop inside the same bot.event decorator
- Tested the bot on 2 test servers

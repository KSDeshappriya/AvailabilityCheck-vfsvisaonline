### Step-by-step Guide:

1. **Set Up the Bot with Pyrogram**:
   - First, ensure you have Pyrogram installed and a bot token from the Telegram BotFather.

   ```bash
   pip install pyrogram
   ```

   ```bash
   pip install -r requirements.txt
   ```

   - You should create Cred.py. Like this,
        ```python
        class Cred:
            # For authentications
            API_ID =   # Telegram API ID
            API_HASH =   # Telegram API Hash
            BOT_TOKEN =  # Telegram Bot Token
        ```

To check for appointments every 60 seconds, you can run the `check_appointments` function periodically using Python's `asyncio` and scheduling methods. Since you're working within Pyrogram, which is asynchronous, it’s important to set up a background task that triggers the check every 60 seconds.

Here’s how you can modify your bot to include periodic checks:

### Steps to Implement Periodic Checks:

1. **Use `asyncio` to Run a Task Periodically**:
   Pyrogram works with `asyncio`, so you can schedule a task to run every 60 seconds.

2. **Create a Background Task**:
   You can run a background task within Pyrogram using `asyncio.create_task`.

3. **Notify the User Periodically**:
   When new updates or appointment slots are available, you can send the information to the user.

### Key Changes:
1. **Global `user_chat_id`:**
   - A global variable `user_chat_id` is used to store the ID of the user to whom appointment updates will be sent periodically.

2. **`check_appointments_periodically` Function:**
   - This function runs an infinite loop (`while True`) and checks for appointments every 60 seconds using `asyncio.sleep(60)` to pause the loop.
   - The function sends messages to the user with the result of each check.

3. **`/start` Command:**
   - When the user sends the `/start` command, their chat ID is saved, and the periodic checking starts with `asyncio.create_task`.
   
4. **`/stop` Command:**
   - This command allows the user to stop the periodic checking by setting `user_chat_id` to `None`.

### Summary of the Flow:
- When the user sends `/start`, the bot will begin checking for appointments every 60 seconds and sending updates to the user.
- If the user wants to stop receiving periodic updates, they can send the `/stop` command.
# Slack-User-Message-Filter
Extracts and exports Slack messages for a specific user within a date range from JSON logs to CSV.


# Slack User Message Filter

This script filters and extracts Slack messages sent by a specific user within a specified date range from a collection of exported Slack JSON logs. It organizes the results and exports them to a clean, structured CSV file.

---

## Features

- Recursively processes all `.json` files in a given folder
- Filters messages by:
  - Target `user_id`
  - Date range (e.g. `2024-08-10` to `2025-03-10`)
- Handles both individual and list-style JSON formats
- Converts Slack timestamps into readable `HH:MM:SS`
- Outputs to a CSV with columns like `Date`, `Time`, `User`, `Text`, etc.
- Sorts messages by folder, date, and time

---

##  Input

- Folder containing exported Slack `.json` logs (e.g. `conversation_only`)
- Slack messages must include fields like `"user"`, `"text"`, and `"ts"`

---

##  Output

- A single CSV file (e.g., `conversation_only.csv`) with filtered messages from the target user.

---

##  Configuration

Update these values at the top of the script:

```python
folder_path = "/your/path/to/json/files"
output_csv = "conversation_only.csv"
target_user = "USER_ID"  # Replace with actual Slack user ID

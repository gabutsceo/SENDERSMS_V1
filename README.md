"""

## Use This Domain Inbox

xdz.ai

https://ghss.ai/5digit
.co
.cc
.inc

## HOW TO USE

This guide explains how to set up and run the script to send emails or SMS messages using dynamic links and rotating content.

---

### File Structure

The script relies on several input files to work. Below is the file structure and their purposes:

#### `assets/actual_links.txt`

A file containing the links to be used in the subject and message content. Each line should be a valid URL. Example:
xdz.ai/FNWtv
xdz.ai/FgGat
xdz.ai/rMT9I

#### `assets/users.txt`

A file containing SMTP user credentials in the format:
email1@example.com,password1
email2@example.com,password2

#### `assets/list.txt`

A file containing recipient details (number and carrier) in the format:
1234567890,carrier1
0987654321,carrier2

#### `assets/subject.txt`

A file containing rotating subjects. Use `{{link}}` as a placeholder for dynamic links. Example:
(amazon.com Sign-In) Unusual login detected. Was this you? Visit {{link}}

#### `assets/content.txt`

A file containing rotating email/SMS content. Use `{{link}}` as a placeholder for dynamic links. Example:
We noticed an unusual login attempt. If this was you, confirm here: {{link}}

---

### Configuration Parameters

- **`DELAY_SECONDS`**: Time (in seconds) between batches of messages. Default is `10`.
- **`BATCH_SIZE`**: Number of recipients processed per batch. Default is `10`.

---

### Running the Script

1. Install required modules:pip install smtplib,pip install logging

2. Save this script as `main.py`.

3. Ensure all required files are placed in the `assets` directory.

4. Run the script using:

```bash
python main.py
```

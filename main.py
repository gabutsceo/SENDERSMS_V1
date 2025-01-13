import multiprocessing
from SquidSMS import SquidSMS
import time
import random
from itertools import cycle
import requests
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

# Gmail Configuration
DELAY_SECONDS = 2  # Delay between emails (10 seconds after success)
BATCH_SIZE = 10 # Process two recipients at a time per batch

# Proxy Configuration (Updated)
username = "52xrymt17qdjxdn"
password = "00h90dhkmyeephq"
proxy_host = "rp.proxyscrape.com:6060"
proxy_auth = f"{username}:{password}@{proxy_host}"

proxies = [f"http://{proxy_auth}"]  # Single proxy configuration
proxy_cycle = cycle(proxies)  # Maintain the same logic for cycling, though only one proxy exists


# Helper functions
def load_file(file_name):
    """Load lines from a file and strip whitespace."""
    with open(file_name, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def rotate_content(content, placeholders):
    """Replace placeholders in content with dynamic values."""
    for placeholder, replacement in placeholders.items():
        content = content.replace(placeholder, replacement)
    return content

# Load data
actual_links = load_file('assets/actual_links.txt')  # Links to use in subject and content
users = [line.split(',') for line in load_file('assets/users.txt')]  # SMTP users
recipients = [line.split(',') for line in load_file('assets/list.txt')]  # Recipient number and carrier
subjects = load_file('assets/subject.txt')  # Rotating subjects
contents = load_file('assets/content.txt')  # Rotating email contents

# Setup cycles
user_cycle = cycle(users)
actual_link_cycle = cycle(actual_links)
subject_cycle = cycle(subjects)
content_cycle = cycle(contents)

# Color function
def get_color_for_process(process_id):
    """Assign a unique color to each process."""
    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.CYAN, Fore.MAGENTA, Fore.WHITE]
    return colors[process_id % len(colors)]

def send_email_sms(process_id, recipients_subset, smtp_user):
    # Assign a unique color for the process
    color = get_color_for_process(process_id)

    try:
        # Ensure `smtp_user` is unpacked correctly
        user, password = smtp_user
        proxy_url = next(proxy_cycle)

        # Assign unique subject and content
        subject = next(subject_cycle)
        content = next(content_cycle)
        current_link = next(actual_link_cycle)

        placeholders = {"{{link}}": current_link}
        content_with_placeholders = rotate_content(content, placeholders)

        print(f"{color}Process {process_id} | SMTP User: {user} | Proxy: {proxy_url}")

        # Initialize SquidSMS
        example = SquidSMS(user, password)
        server = example.connect()

        # Prepare recipients for BCC
        primary_recipient = recipients_subset[0]
        bcc_recipients = [
            f"{number}{example.CARRIERS[carrier]}"
            for number, carrier in recipients_subset[1:]
        ]

        # Prepare email message
        email_message = f"Subject: {subject}\n\n{content_with_placeholders}"

        # Send email with BCC
        result = example.send(
            server,
            primary_recipient[0],  # Phone number of primary recipient
            primary_recipient[1],  # Carrier of primary recipient
            email_message,
            bcc=bcc_recipients
        )

        if result:
            print(f"{color}Process {process_id}: Email sent successfully to BCC recipients.")
        else:
            print(f"{color}Process {process_id}: Failed to send email.")

        example.disconnect(server)
        time.sleep(DELAY_SECONDS)

    except Exception as e:
        print(f"{color}Process {process_id}: Error occurred: {e}")



# Function to handle batching
def process_batch(batch_number, start_index):
    print(f"Starting Batch {batch_number}...")
    batch_recipients = recipients[start_index:start_index + BATCH_SIZE]

    processes = []
    for i in range(0, len(batch_recipients), 10):  # Group into batches of 10
        bcc_group = batch_recipients[i:i + 10]
        if len(bcc_group) < 2:
            continue  # Skip if not enough recipients for BCC

        process = multiprocessing.Process(
            target=send_email_sms,
            args=(i + 1, bcc_group, next(user_cycle))
        )
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print(f"Batch {batch_number} completed.")
    time.sleep(DELAY_SECONDS)



if __name__ == "__main__":
    user_input = input("Do you want to use a proxy? (yes/no): ").strip().lower()
    use_proxy = user_input == 'yes'

    # Ask user if they want to send emails one by one or in parallel
    mode_input = input("Do you want to send emails one by one (type 'single') or using multiple processes (type 'multi')? ").strip().lower()

    if mode_input == 'single':
        # Ambil SMTP user dari user_cycle
        smtp_user = next(user_cycle)
        # Kirim email untuk satu proses saja
        send_email_sms(1, recipients[:1], smtp_user)

    elif mode_input == 'multi':
        # Multi-process (sending emails in parallel) with batches
        num_batches = len(recipients) // BATCH_SIZE
        for batch_number in range(num_batches):
            start_index = batch_number * BATCH_SIZE
            process_batch(batch_number + 1, start_index)

        print("All email sending processes completed.")
    else:
        print("Invalid input. Please choose 'single' or 'multi'.")

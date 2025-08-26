import requests
import subprocess
import time

BOT_TOKEN = '7937745403:AAHqY9ht3SlaAtc32rQZ4T_l_bUbmbM2prE'
CHAT_ID = '6601930239'
VPS_FILE = 'vps.txt'

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("Message sent successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")

def get_tmate_link():
    try:
        process = subprocess.Popen(['tmate', '-F', '#{tmate_ssh}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(timeout=10)
        if process.returncode == 0:
            return stdout.decode('utf-8').strip()
        else:
            print(f"Error getting tmate link: {stderr.decode('utf-8')}")
            return None
    except subprocess.TimeoutExpired:
        process.kill()
        print("tmate command timed out.")
        return None
    except FileNotFoundError:
        print("tmate command not found. Please ensure tmate is installed and in your PATH.")
        return None

if __name__ == '__main__':
    tmate_link = None
    for _ in range(5): # Try a few times to get the tmate link
        tmate_link = get_tmate_link()
        if tmate_link:
            break
        time.sleep(2)

    if tmate_link:
        print(f"Tmate link: {tmate_link}")
        with open(VPS_FILE, 'w') as f:
            f.write(tmate_link)
        send_telegram_message(f"Tmate SSH link: {tmate_link}")
    else:
        print("Failed to get tmate link after multiple attempts.")
        send_telegram_message("Failed to start tmate session and get link.")

    # Keep the script running for Railway to keep the container alive
    while True:
        time.sleep(3600) # Sleep for an hour


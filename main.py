from requests import post
from user_agent import generate_user_agent
from colorama import Fore, init
from os import system, name
from concurrent.futures import ThreadPoolExecutor
from time import time, sleep
from datetime import timedelta
import sys
import json

try:
    from pystyle import Colors, Colorate, Center
except ImportError:
    class Colors:
        red_to_blue = "" 
    class Colorate:
        @staticmethod
        def Diagonal(color, text):
            return text
    class Center:
        @staticmethod
        def XCenter(text):
            return text 

init()

g = Fore.GREEN
w = Fore.WHITE
r = Fore.RED
re = Fore.RESET
y = Fore.YELLOW

class Counter:
    def __init__(self):
        self.value = 0
        self.start_time = time()

    def increment(self):
        self.value += 1
        
    def get_elapsed_time(self):
        return timedelta(seconds=int(time() - self.start_time))

def show_banner():
    print(Colorate.Diagonal(Colors.red_to_blue, Center.XCenter("""


▗▖ ▗▖▗▄▄▄▖▗▄▄▖ ▗▖ ▗▖ ▗▄▖  ▗▄▖ ▗▖ ▗▖     ▗▄▄▖▗▄▄▖  ▗▄▖ ▗▖  ▗▖▗▖  ▗▖▗▄▄▄▖▗▄▄▖ 
▐▌ ▐▌▐▌   ▐▌ ▐▌▐▌ ▐▌▐▌ ▐▌▐▌ ▐▌▐▌▗▞▘    ▐▌   ▐▌ ▐▌▐▌ ▐▌▐▛▚▞▜▌▐▛▚▞▜▌▐▌   ▐▌ ▐▌
▐▌ ▐▌▐▛▀▀▘▐▛▀▚▖▐▛▀▜▌▐▌ ▐▌▐▌ ▐▌▐▛▚▖      ▝▀▚▖▐▛▀▘ ▐▛▀▜▌▐▌  ▐▌▐▌  ▐▌▐▛▀▀▘▐▛▀▚▖
▐▙█▟▌▐▙▄▄▖▐▙▄▞▘▐▌ ▐▌▝▚▄▞▘▝▚▄▞▘▐▌ ▐▌    ▗▄▄▞▘▐▌   ▐▌ ▐▌▐▌  ▐▌▐▌  ▐▌▐▙▄▄▖▐▌ ▐▌
                                                                            
                               t.me/secabuser                    
""")))
def clear_screen():
    system('cls' if name == 'nt' else 'clear')

def show_results(counter, webhook_url, message_content, total_sends_requested):
    clear_screen()
    show_banner()
    
    display_webhook_url = webhook_url if len(webhook_url) <= 30 else webhook_url[:27] + "..."
    display_message_content = message_content if len(message_content) <= 30 else message_content[:27] + "..."

    results_box = f"""
╔{'═'*40}╗
║{' RESULTS   '.center(38)}  ║
╠{'═'*40}╣
║ Message >  {display_message_content.ljust(28)}║
║ Requested Sends >  {str(total_sends_requested).ljust(20)}║
║ Successful Sends > {str(counter.value).ljust(20)}║
║ Elapsed Time >{str(counter.get_elapsed_time()).ljust(24)} ║
╚{'═'*40}╝
"""
    print(Colorate.Diagonal(Colors.red_to_blue, Center.XCenter(results_box)))

def send_webhook_message(webhook_url, message, username="Webhook Spammer", avatar_url=None):
    headers = {
        "User-Agent": generate_user_agent(),
        "Content-Type": "application/json"
    }
    payload = {
        "content": message,
        "username": username,
        "avatar_url": avatar_url
    }
    return post(webhook_url, json=payload, headers=headers)

def spam_webhook(webhook_url, message_content, counter, total_sends_requested, delay_per_send, username):
    if counter.value >= total_sends_requested:
        return

    try:
        response = send_webhook_message(webhook_url, message_content, username=username)
        
        if response.status_code in [200, 204]:
            print(f"{g}Webhook Sent | ({response.status_code}){re}")
            counter.increment()
        elif response.status_code == 429:
            try:
                retry_after = response.json().get('retry_after') / 1000.0
                print(f"{y}Rate Limited! Retrying after {retry_after:.2f} seconds...{re}")
                sleep(retry_after)
                response = send_webhook_message(webhook_url, message_content, username=username)
                if response.status_code in [200, 204]:
                    print(f"{g}Webhook Sent (after retry) | ({response.status_code}){re}")
                    counter.increment()
                else:
                    print(f"{r}Webhook Not Sent (after retry) | ({response.status_code}) - {response.text}{re}")
            except (json.JSONDecodeError, AttributeError):
                print(f"{r}Rate Limit error, but could not parse retry_after. Waiting 5 seconds.{re}")
                sleep(5)
                print(f"{r}Webhook Not Sent | ({response.status_code}) - {response.text}{re}")
        else:
            print(f"{r}Webhook Not Sent | ({response.status_code}) - {response.text}{re}")
    except Exception as e:
        print(f"{r}Error Sending Webhook > {str(e)}{re}")
    
    if delay_per_send > 0:
        sleep(delay_per_send)
        

def main():
    clear_screen()
    show_banner()
    
    try:
        webhook_url = input(f'{w}Webhook > {re}').strip() # Webhook Url
        if not webhook_url or not webhook_url.startswith("https://discord.com/api/webhooks/"):
            print(f"{r}Invalid Discord Webhook URL. Please enter a valid URL. :] {re}")
            sys.exit(1)

        message_content = input(f'{w}Message > {re}').strip() # Message Spam
        if not message_content:
            print(f"{r}koni mesl adam  :] {re}")
            sys.exit(1)

        username_input = input(f'{w}Username > {re}').strip()
        if not username_input:
            username_input = "Webhook Spammer" # UserName Webhook
        
        try:
            total_sends_requested = int(input(f'{w}Total Messages > {re}') or 10) # Totol(number) Message
            if total_sends_requested < 1:
                print(f"{r}Total messages to send must be 1 or more :] {re}")
                sys.exit(1)
        except ValueError:
            print(f"{r}Invalid number for total messages :] {re}")
            sys.exit(1)

        try:
            max_threads = int(input(f'{w}Threads > {re}') or 5) # Max Treads
            if max_threads < 1:
                print(f"{r}Threads must be 1 or more :] {re}")
                sys.exit(1)
        except ValueError:
            print(f"{r}Invalid threads number :] {re}")
            sys.exit(1)

        try:
            delay_per_send = float(input(f'{w}Delay > {re}') or 0.1) # Sleep Time
            if delay_per_send < 0:
                print(f"{r}Delay cannot be negative :] {re}")
                sys.exit(1)
        except ValueError:
            print(f"{r}Invalid delay time :] {re}")
            sys.exit(1)

        clear_screen()
        show_banner()
        
        counter = Counter()
        
        print(f"\n{w}Starting Webhook Spam... (Sending {total_sends_requested} messages)\n")
        
        while counter.value < total_sends_requested:
            remaining_sends = total_sends_requested - counter.value
            threads_to_run = min(max_threads, remaining_sends)

            if threads_to_run == 0:
                break

            with ThreadPoolExecutor(max_workers=threads_to_run) as executor:
                futures = [
                    executor.submit(
                        spam_webhook, webhook_url, message_content, counter,
                        total_sends_requested, delay_per_send, username_input
                    )
                    for _ in range(threads_to_run)
                ]
                for f in futures:
                    f.result()
            
    except KeyboardInterrupt:
        print(f"\n{r}Spamming cancelled by user :] {re}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{r}An unexpected error occurred > {e}{re}")
        sys.exit(1)
    finally:
        show_results(counter, webhook_url, message_content, total_sends_requested)

if __name__ == "__main__":
    main()

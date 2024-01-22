import os
import socket
import codecs
import requests
from io import StringIO
import csv

def download_domains_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error downloading domain list from URL: {e}")
        return None

def check_connection(domain):
    if not domain:
        return False  # Skip empty domains

    try:
        # Skip TLDs without a specific domain
        if domain.startswith('.'):
            return False

        # Encode the domain using 'idna' encoding
        encoded_domain = codecs.encode(domain, 'idna').decode('utf-8')
        socket.create_connection((encoded_domain, 80), timeout=5)
        return True
    except (socket.timeout, socket.error):
        return False
    except UnicodeError:
        print(f"Skipping domain {domain} due to encoding error.")
        return False

def write_successful_connections(successful_connections):
    with open('successful_connections.txt', 'w', encoding='utf-8') as file:
        file.write('\n'.join(successful_connections))

def print_summary(successful_connections):
    total_successful = len(successful_connections)

    print(f"\nSummary:")
    print(f"Successful ({total_successful}):")
    
    for domain in successful_connections:
        print(domain)

def main():
    # Define the URL to fetch the domain list
    domain_list_url = "https://gist.githubusercontent.com/derlin/421d2bb55018a1538271227ff6b1299d/raw/3a131d47ca322a1d001f1f79333d924672194f36/country-codes-tlds.csv"

    # Download domain list from the URL
    domain_list_text = download_domains_from_url(domain_list_url)

    if not domain_list_text:
        return

    # Read domains from the CSV data
    csv_reader = csv.reader(StringIO(domain_list_text))
    domains = [row[-1] for row in csv_reader]

    # List to store successful connections
    successful_connections = []

    # Check connection for each domain
    for domain in domains:
        if check_connection(domain):
            print(f"Connection to {domain} successful.")
            successful_connections.append(domain)
        else:
            print(f"Connection to {domain} failed.")

    # Write successful connections to a file
    write_successful_connections(successful_connections)

    # Print summary
    print_summary(successful_connections)

if __name__ == "__main__":
    main()

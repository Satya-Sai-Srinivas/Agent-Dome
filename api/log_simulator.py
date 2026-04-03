import json
import random
import time
from faker import Faker 

# Initialize Faker to generate realistic network data
fake = Faker()

def generate_log():
    """
    Generates a single fake web server log.
    Simulates a 95% benign / 5% malicious traffic split.
    """
    # Generate a random number between 0.0 and 1.0. 
    # If it's less than 0.05 (5%), we trigger an attack.
    is_malicious = random.random() < 0.05 
    
    # Generate realistic base data for every request
    ip_address = fake.ipv4()
    timestamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    user_agent = fake.user_agent()
    
    if is_malicious:
        # These are the exact payloads we will train the AI to catch later
        attack_payloads = [
            "GET /login?user=' OR 1=1-- HTTP/1.1",              # SQL Injection
            "GET /../../../../etc/passwd HTTP/1.1",             # Directory Traversal
            "POST /api/admin/exec?cmd=rm -rf / HTTP/1.1",       # Command Injection
            "GET /search?q=<script>alert('XSS')</script> HTTP/1.1" # Cross-Site Scripting (XSS)
        ]
        request_string = random.choice(attack_payloads)
        # Attacks often result in 403 Forbidden or 500 Internal Server Error
        status_code = random.choice([200, 403, 500]) 
    else:
        # Normal, boring web traffic requesting random pages
        request_string = f"GET /{fake.uri_path()} HTTP/1.1"
        status_code = 200
        
    # Structure the log exactly how enterprise SIEMs (like Splunk) expect it
    log_entry = {
        "timestamp": timestamp,
        "source_ip": ip_address,
        "request": request_string,
        "status": status_code,
        "user_agent": user_agent,
        "is_attack_simulation": is_malicious # Helpful flag for us while building
    }
    
    return log_entry

if __name__ == "__main__":
    print("🛡️ Starting Cyber-Sentinel Mock Log Generator...")
    print("Press Ctrl+C to stop.")
    print("-" * 60)
    
    try:
        while True:
            # Generate the log dictionary
            new_log = generate_log()
            
            # Convert the Python dictionary to a formatted JSON string and print it
            print(json.dumps(new_log, indent=2))
            
            # Pause for a random amount of time (between 0.5 and 1.5 seconds) 
            # to make the traffic flow look like real humans clicking around
            time.sleep(random.uniform(0.5, 1.5))
            
    except KeyboardInterrupt:
        print("\n🛑 Simulator stopped securely.")
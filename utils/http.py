import random
import os

def get_random_user_agent():
    filename = random.choice([f for f in os.listdir("../assets/useragents") 
                                if not f.startswith('.')])
    with open(f"../assets/useragents/{filename}") as file:
        line = file.readlines()
        return random.choice(line).split('\n')[0]

def get_request_headers():
    headers={
        'User-Agent' : get_random_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Accept-Encoding':'gzip, deflate, br'
    }
    return headers

# if __name__ == '__main__':
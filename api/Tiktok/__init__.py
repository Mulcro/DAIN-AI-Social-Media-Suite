import urllib
from api import exchange_code_for_access_token, upload_video
# import random
import os 
from dotenv import load_dotenv 

# Tiktok access token ( must be obtianed via Oauth2 )

load_dotenv()

CLIENT_KEY = os.getenv("TIKTOK_CLIENT_KEY")

SERVER_ENDPOINT_REDIRECT = "https://7beb-134-xxx-xx.ngrok.io/callback"

def generate_auth_url():
    # randomly generate numbers for forgery token
    csrfState = 0
    # get the base uri
    url = 'https://www.tiktok.com/v2/auth/authorize/'

    # add all the parameters that we need
    url += f'?client_key={CLIENT_KEY}' 
    url += f'&scope=video.publish'
    url += f'&response_type=code'
    url += f'&redirect_uri={SERVER_ENDPOINT_REDIRECT}'
    url += '&state=' + str(csrfState)
    
    

    # return the url
    return (url, csrfState) 


def main_tests():
     # Generate authorization URL
    print("Generating authorization URL...")
    url, state = generate_auth_url()
    print("URL:", url)
    print("State:", state)
    
    # Prompt user for the redirect URL
    input_ = input("Paste the URL you were redirected to: ")
    
    # Extract authorization code from redirect URL
    response = input_.split("code=")[1].split("&")[0]

    # Decode the code (THAT'S THE EDITING PART)
    decoded_code = urllib.parse.unquote(response)

    print("Code:", response)
    print("Decoded Code:", decoded_code)
    return decoded_code


if __name__ == "__main__":
    # Exchange code (from URL param)
    # Step 1: make call to tiktok for the authorization code
    code = main_tests()
    # Step 2: exchange code for access token
    response = exchange_code_for_access_token(code)
    access_token = response.get("access_token")


    # Step 3: Upload video
    result = upload_video(access_token, "video/tiktok.mp4")

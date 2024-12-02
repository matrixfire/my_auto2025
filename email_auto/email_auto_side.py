import requests
import time

def verify_email(email, api_key):
    url = "https://api.hunter.io/v2/email-verifier"
    params = {
        "email": email,
        "api_key": api_key
    }
    headers = {
        "Accept": "application/json"
    }

    response = requests.get(url, params=params, headers=headers)

    # Check if the response status code is 202 (Accepted)
    if response.status_code == 202:
        # If the response code is 202, it means the request is being processed.
        # We need to poll the endpoint until we get a response.
        retry_after = 20  # Retry after 20 seconds
        time.sleep(retry_after)
        response = requests.get(url, params=params, headers=headers)

    # Check if the response status code is 200 (OK)
    if response.status_code == 200:
        remaining_requests = int(response.headers.get('X-Rate-Limit-Remaining', -1))
        print(f"Remaining requests: {remaining_requests}")
        
        data = response.json()
        # Check if the request was successful
        if data["data"]["status"] == "valid":
            return True, data["data"]
        else:
            return False, data["data"]
    else:
        # Request failed
        return False, {"error": f"Failed to verify email. Status code: {response.status_code}"}

# Example usage:
email = "matrixbox@qq.com"
api_key = "114726e297ae3f374e1b029028a7449bd704117a"

valid, verification_data = verify_email(email, api_key)
if valid:
    print("Email is valid!")
    print("Verification details:", verification_data)
else:
    print("Email is not valid.")
    print("Error details:", verification_data)



def rename_files(folder_path):
    for filename in os.listdir(folder_path):
        if "飞机" in filename:
            new_filename = filename.replace("飞机", "Helicopter")
            os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
    for filename in os.listdir(folder_path)
        if "说明书" in filename:
            new_filename = filename.replace("说明书", "Manual")
            os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))


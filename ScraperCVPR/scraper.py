import requests

# URL of the target website
url = "https://openaccess.thecvf.com/CVPR2024?day=all"

try:
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Save the raw HTML content to a file
        with open("cvpr2024_raw.html", "w", encoding="utf-8") as file:
            file.write(response.text)
        print("HTML content downloaded and saved as 'cvpr2024_raw.html'.")
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

except Exception as e:
    print(f"An error occurred: {e}")

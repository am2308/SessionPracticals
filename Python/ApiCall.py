import requests
import json

def fetch_data(api_url, output_file):
    try:
        # Send a GET request to the API
        response = requests.get(api_url)
        
        # Raise an error for bad responses
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        
        # Write the JSON data to a file
        with open(output_file, 'w') as file:
            json.dump(data, file, indent=4)  # Pretty print with indentation
        
        print(f"Data successfully written to {output_file}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
    except json.JSONDecodeError:
        print("Error decoding JSON response.")
    except IOError as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    # Specify the API URL and output file
    api_url = "https://restcountries.com/v3.1/all"  # Replace with your API URL
    output_file = "output.json"  # Desired output file name

    fetch_data(api_url, output_file)

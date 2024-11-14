import requests
from bs4 import BeautifulSoup
import json
import time
import random


class WebTools:
    def __init__(self, bing_api_key, num_urls=3, proxies=None):
        self.bing_api_key = bing_api_key
        self.num_urls = num_urls
        self.proxies = proxies
        self.bing_url = "https://api.bing.microsoft.com/v7.0/search"

    def search_web(self, query):
        """
        Searches the web using Bing Search API and returns the first N URLs based on the query.
        """
        headers = {
            'Ocp-Apim-Subscription-Key': self.bing_api_key
        }
        params = {
            'q': query,
            'count': self.num_urls
        }

        # Random delay between requests to avoid bot detection
        time.sleep(random.uniform(1, 3))

        try:
            response = requests.get(self.bing_url, headers=headers, params=params, proxies=self.proxies)
            response.raise_for_status()

            if response.status_code == 200:
                results = response.json()
                # Extract URLs from results - accounting for Bing's response format
                urls = [result.get('url') for result in results.get('webPages', {}).get('value', []) if
                        result.get('url')]
                return urls
            else:
                raise Exception(f"Error searching web: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Error making request to Bing: {str(e)}")

    def extract_text_from_url(self, url):
        """
        Extracts and returns the main text content from the given URL.
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15'
        }
        try:
            response = requests.get(url, headers=headers, proxies=self.proxies)
            response.raise_for_status()

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                paragraphs = soup.find_all('p')
                text = ' '.join([para.get_text() for para in paragraphs])
                return text
            else:
                raise Exception(f"Error fetching URL content: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching URL: {str(e)}")

    def consolidate_text_from_results(self, query):
        """
        Searches the web for a query and extracts consolidated text from all search results,
        appending reference information at the end of each page's text.
        """
        urls = self.search_web(query)
        consolidated_text = ""

        for url in urls:
            try:
                text = self.extract_text_from_url(url)
                consolidated_text += f"\n\n--- Content from: {url} ---\n{text}"
            except Exception as e:
                consolidated_text += f"\n\n--- Failed to extract content from: {url} ---\n{str(e)}"

        return consolidated_text


# Example usage
if __name__ == "__main__":
    query = "Impact of AI on developer jobs"
    bing_api_key = "YOUR_BING_API_KEY"  # Replace with your actual Bing Search API key

    # Define a proxy if needed
    proxies = {
        'http': 'http://your.proxy.ip:port',
        'https': 'http://your.proxy.ip:port',
    }

    web_tools = WebTools(bing_api_key=bing_api_key, num_urls=3, proxies=proxies)

    try:
        urls = web_tools.search_web(query)
        print("Top URLs:", urls)

        # Extract and print text from the first URL
        if urls:
            text_content = web_tools.extract_text_from_url(urls[0])
            print("Extracted Text:", text_content[:500], "...")

        # Extract and print consolidated text from all search results
        consolidated_text_content = web_tools.consolidate_text_from_results(query)
        print("\nConsolidated Text from All Results:", consolidated_text_content[:1000], "...")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

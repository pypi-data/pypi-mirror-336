from promptflow import tool
from promptflow.connections import CustomConnection
import requests
from bs4 import BeautifulSoup
import json
def bing_search(query, num_results=10):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    search_url = f"https://www.bing.com/search?q={query}"
    
    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        for item in soup.find_all('li', class_='b_algo')[:num_results]:
            title = item.find('h2')
            link = title.find('a')['href'] if title else None
            snippet = item.find('p').text.strip() if item.find('p') else ''
            
            if link:
                results.append({
                    'title': title.text.strip(),
                    'link': link,
                    'snippet': snippet
                })
        
        return results

    except Exception as e:
        print(f"搜索时发生错误：{e}")
        return []
@tool
def search(connection: CustomConnection, input_text: str) -> str:
    # Replace with your tool code.
    # Usually connection contains configs to connect to an API.
    # Use CustomConnection is a dict. You can use it like: connection.api_key, connection.api_base
    # Not all tools need a connection. You can remove it if you don't need it.
    return json.dumps(bing_search(input_text))
# File: fbi-wanted-library/fbi-wanted-library/fbi_wanted_library/fbi_wanted.py

import requests
import asyncio
import math

API_URL = "https://api.fbi.gov/wanted/v1/list"

class FBIWanted:
    @staticmethod
    def search(name: str = None, race: str = None, hair_colour: str = None, eye_colour: str = None, sex: str = None, field_offices: str = None) -> list:
        """
        Run search in an event loop with optional filters.
        """
        # Create a dictionary of query parameters
        params = {
            "title": name,  # Rename 'name' to 'title'
            "race": race,
            "hair": hair_colour,  # Rename 'hair_colour' to 'hair'
            "eye": eye_colour,  # Rename 'eye_colour' to 'eye'
            "sex": sex,
            "field_offices": field_offices
        }

        # Remove any keys with None values
        params = {key: value.lower() for key, value in params.items() if value is not None}

        # Pass the params to the asynchronous search function
        results = asyncio.run(FBIWanted._search(params))
        return results

    @staticmethod
    async def _search(params: dict) -> list:
        """Fetch all paginated results from the FBI Wanted API with filters."""
        results = []  # Initialize an empty list to store all results

        # Get the first page of results
        data = await FBIWanted._get_results(params, page=1)
        if not data:
            return results

        # Add the items from the first page to the results
        results.extend(data['items'])

        # Calculate the total number of pages, capped at 20
        total_results = data['total']
        total_pages = min(math.ceil(total_results / 50), 20)  # Each page contains 50 items, max 20 pages

        # Create tasks to fetch the remaining pages
        tasks = [
            FBIWanted._get_page(params, page)
            for page in range(2, total_pages + 1)
        ]
        remaining_pages = await asyncio.gather(*tasks)

        # Add the results from the remaining pages
        for page_data in remaining_pages:
            if page_data and 'items' in page_data:
                results.extend(page_data['items'])

        return results

    @staticmethod
    async def _get_results(params: dict, page: int = 1) -> dict | None:
        """Fetch results for a specific page using requests."""
        url = API_URL
        params["page"] = page  # Add the page number to the query parameters
        params["pageSize"] = 50  # Set the page size to 50

        try:
            # Use requests to fetch the data
            response = await asyncio.to_thread(requests.get, url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: Received status code {response.status_code}")
                return None
        except Exception as e:
            print("Error:", e)
            return None

    @staticmethod
    async def _get_page(params: dict, page: int) -> dict | None:
        """Fetch a specific page of results."""
        return await FBIWanted._get_results(params, page=page)
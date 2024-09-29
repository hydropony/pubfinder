import requests
import pandas as pd
import time
import os
from dotenv import load_dotenv

load_dotenv()
# Your Google Places API key
PLACES_API_KEY = os.getenv('PLACES_API_KEY') 

# Function to search for pubs in a city
def search_pubs_in_city(city_name, radius=7000, maxplaces=600):
  placetypes = ['bar', 'pub', 'nightlife', 'karaoke', 'club', 'cafe', 'beer', 'wine', 'cocktail', 'biljard', 'billiard']
  pubs = []
  pubsset = set()
  for placetype in placetypes:
    page = 0
    print(f'Searching for {placetype}')
    search_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
      'query': f'{placetype} in {city_name}',
      'radius': radius,
      # 'type': placetype,  # 'bar' or 'pub'
      'key': PLACES_API_KEY
    }
    
    while True:
      print(f'page {page}')
      response = requests.get(search_url, params=params)
      data = response.json()
      results = data.get('results')

      for pub in results:
        if (len(pubs) > maxplaces):
          print(f'places found: {len(pubs)}')
          return pubs

        if (pub['name'] in pubsset):
          continue
        else:
          pubsset.add(pub['name'])
        
        pubs.append({
          'name': pub['name'],
          'address': pub.get('formatted_address'),
          'place_id': pub['place_id'],
          'rating': pub.get('rating'),
          'total_ratings': pub.get('user_ratings_total')
        })
      
      next_page_token = data.get('next_page_token')
      if next_page_token:
        params['pagetoken'] = next_page_token
        page += 1
        # Sleep to respect API rate limits (next_page_token takes a couple of seconds to become valid)
        time.sleep(2)
      else:
        print(f'places found: {len(pubs)}')
        break
    print()
  return pubs

# Function to get reviews for a specific pub using place_id
def get_pub_reviews(place_id):
    details_url = f"https://maps.googleapis.com/maps/api/place/details/json"
    params = {
      'place_id': place_id,
      'fields': 'name,rating,reviews',
      'key': PLACES_API_KEY
    }
    
    response = requests.get(details_url, params=params)
    result = response.json().get('result')
    
    reviews = []
    if 'reviews' in result:
        for review in result['reviews']:
            reviews.append({
                'author': review['author_name'],
                'rating': review['rating'],
                'text': review['text'],
                'time': review['relative_time_description']
            })
    
    return reviews

# Main function to search pubs and get their reviews
def get_pubs_and_reviews(city_name):
    pubs = search_pubs_in_city(city_name)
    all_pubs_reviews = []
    
    for pub in pubs:
        print(f"Fetching reviews for: {pub['name']}")
        reviews = get_pub_reviews(pub['place_id'])
        pub_data = {
            'name': pub['name'],
            'address': pub['address'],
            'rating': pub['rating'],
            'total_ratings': pub['total_ratings'],
            'reviews': reviews
        }
        all_pubs_reviews.append(pub_data)
        
        # Sleep to respect API rate limits
        time.sleep(4)
    
    return all_pubs_reviews

# Example usage
city_name = 'Helsinki'
# pubs_data = get_pubs_and_reviews(city_name)
# pubs = search_pubs_in_city(city_name)
pubs = pd.read_json('Helsinki_pubs.json')

reviews = get_pub_reviews('ChIJM0I01c0LkkYRj_3qz99nsyM')

# Convert the data into a DataFrame and save to CSV
# df = pd.DataFrame(pubs)
filename = f'{city_name}_reviews.json' 
df = pd.DataFrame(reviews)
df.to_json(filename, index=False)

print(f"Data saved to {filename}")

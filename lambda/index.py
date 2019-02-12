import requests
import json
from bs4 import BeautifulSoup
import re
from datetime import datetime
import os

INVOKED_URL = os.environ[ "invoke-url" ]
SITEMAP_URL = os.environ[ "sitemap-url" ]

def get_page():
  source_url = INVOKED_URL
  target_url = SITEMAP_URL

  source_response = requests.get( source_url )

  source_headers = source_response.headers
  source_date = source_headers[ "Last-Modified" ]

  target_response = requests.get( target_url )

  target_content = BeautifulSoup( target_response.text, "html.parser" )

  result = target_content.findAll( "tr" )

  for sitemap_url in result:
    for link in sitemap_url.findAll( "a", href=True ):
      if link[ "href" ] == source_url:
        print( "Has been found!" )

        link_date = sitemap_url.findAll( "td" )[ 1 ].text
        target_date_formatted = datetime.strptime( link_date, '%Y-%m-%d %H:%M %z' )
        source_date_formatted = datetime.strptime( source_date, '%a, %d %b %Y %H:%M:%S %Z' )

        target_milis = target_date_formatted.timestamp()
        source_milis = source_date_formatted.timestamp() - source_date_formatted.second
        
        if source_milis > target_milis:
          print( "Content must be updated!" )
  

def lambda_handler(event, context):
  get_page()
  return {
        "statusCode": 200,
        "body": json.dumps(
            { "message": "Updated sucessfully" }
        ),
    }

if __name__ == '__main__':
  get_page()
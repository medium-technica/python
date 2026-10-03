import pandas as pd
import requests
from bs4 import BeautifulSoup
import io

def print_decoded_message_from_public_doc_url(url):
    try:
     response = requests.get(url)
     if response.status_code != 200:
        raise Exception(f"Failed to fetch document. Ensure it is public. Status code: {response.status_code}")
     dataframes = pd.read_html(io.StringIO(response.text))
     df = dataframes[0]
     max_x, max_y = 0,0
     for index, row in df.iterrows():
      if index > 0:
       if max_x < int(row[2]):
         max_x = int(row[2])
       if max_y < int(row[0]):
         max_y = int(row[0])
     size_x = max_x+1
     size_y = max_y+1
     char_array = [[' ' for _ in range(size_y)] for _ in range(size_x)]
     for index, row in df.iterrows(): 
      if index > 0:
       char_array[max_x-int(row[2])][int(row[0])] = row[1]
     for i in range(size_x):
      for j in range(size_y):
       print(char_array[i][j], end="")
      print()
    except Exception as e:
        print(f"Error! {e}")



if __name__ == '__main__':
    #url = f"https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub"
    url = f"https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub"
    print_decoded_message_from_public_doc_url(url)
    

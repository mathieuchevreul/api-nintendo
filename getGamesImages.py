import requests
import os

def getNintendoGames(IMAGE_FOLDER) :
    EU_API_GAMES = "http://search.nintendo-europe.com/fr/select"

    PARAMS = {'rows': 9999,
		      'fq': 'type:GAME AND system_type:nintendoswitch* AND product_code_txt:*',
		      'q': '*',
		      'sort': 'sorting_title asc',
		      'start': '0',
		      'wt': 'json',
              'priority' : 'az'
              }

    # execute request
    r = requests.get(url = EU_API_GAMES, params = PARAMS)

    # get response in json format
    data = r.json()

    docs = data.get("response").get("docs")

    print(str(len(docs)) + ' games have been retrieved.')

    #image_urls = list()

    # run over each doc
    for doc in docs:
        game_name = doc.get('title')
        image_url = doc.get('image_url_sq_s')

        if '/' in game_name:
            game_name = game_name.replace('/','')

        image_name = IMAGE_FOLDER + game_name + ".jpg"

        # get the images in folder
        if os.path.exists(IMAGE_FOLDER):
            if not os.path.exists(image_name):
                try:
                    with open(image_name, 'wb') as handler:
                        print(str(game_name) + ' image is downloading.')
                        response = requests.get('http:' + image_url)

                        if not response.ok:
                            print(response)

                        for block in response.iter_content(1024):
                            if not block:
                                break

                            handler.write(block)
                except Exception:
                    continue

        else:
            print('The folder ./images does not exist.')
    
def cleanBlankFiles(IMAGE_FOLDER):

    for file in os.listdir(IMAGE_FOLDER):
        try:
            statinfo = os.stat(IMAGE_FOLDER + file)
            if(statinfo.st_size == 0):
                print("remove file")
                os.remove(IMAGE_FOLDER + file)
        except Exception:
            continue

if __name__ == "__main__":
    IMAGE_FOLDER = "images/"

    getNintendoGames(IMAGE_FOLDER)
    cleanBlankFiles(IMAGE_FOLDER)
    

from mwcleric import AuthCredentials

from wiki_closet_client import WikiClosetClient

credentials = AuthCredentials(user_file='me')

wcc = WikiClosetClient(credentials)

for fc in wcc.all_wikis():
    print(fc.url)

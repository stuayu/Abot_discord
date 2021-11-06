from playlist.jpop import *
from playlist.anime import *


async def ck_data(ck_list:str):
    """要求されたものを返す"""
    if ck_list == 'yoasobi':
        use_play = yoasobi
    elif ck_list == 'first_take':
        use_play = first_take
    elif ck_list == 'porno':
        use_play = porno_g
    elif ck_list == 'anime':
        use_play = anime_Uncategorized
    elif ck_list == 'a_2021_summer':
        use_play = anime_2021_summer
    elif ck_list == 'ikimono':
        use_play = ikimono
    elif ck_list == 'yorushika':
        use_play = yorushika
    else:
        use_play = yoasobi + first_take + porno_g + anime_Uncategorized + anime_2021_summer + ikimono + yorushika
    
    return use_play
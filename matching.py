import pandas as pd
def mix_players(information):
    import random
    available_ids = list(information.keys())
    for key in information.keys():
        player_receiver = random.choice(available_ids)
        while player_receiver == key:
            player_receiver = random.choice(available_ids)
        information[key]['receiver'] = player_receiver
        information[player_receiver]['santa'] = key
        available_ids.remove(player_receiver)
    #dict_players = pd.DataFrame(information).T
    #dict_players.to_csv("dictionary.csv")
    return information



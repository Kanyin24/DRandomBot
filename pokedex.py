import requests
import discord

pokemon = 'bulbasaur'

# to get mega pokemon -> https://pokeapi.co/api/v2/pokemon/venusaur-mega

# replace vine-whip by move
url_move = 'https://pokeapi.co/api/v2/move/vine-whip/'
# replace pokemon name by pokemon -> gives info about egg group, base happiness, capture rate, evolved from, mega evo etc.
url_specie = 'https://pokeapi.co/api/v2/pokemon-species/'
# evolution chain -> replace number by id
url_evolution = 'https://pokeapi.co/api/v2/evolution-chain/1/'
# where to encounter the pokemon
url_encounter = 'https://pokeapi.co/api/v2/pokemon/bulbasaur/encounters'
# pokemon basic info url
url_pokemon = 'https://pokeapi.co/api/v2/pokemon/' # + pokemon name
# pokemon types -> double damage / half damage
url_type = 'https://pokeapi.co/api/v2/type/grass/'

def pokemon_basic_info(pokemon):

    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}", headers={"Accept": "application/json"}).json()
    response_specie = requests.get(url_specie+pokemon, headers={"Accept": "application/json"}).json()
    
    embed = discord.Embed(
        title=pokemon,
        color=discord.Color.blurple()
    )

    print(response_specie['base_happiness'])
    print(response_specie['capture_rate'])

    # getting pokemon id
    id = response['id']

    # name of the pokemon
    name = response['name']

    # weight of pokemon
    weight = response['weight']

    # base happiness 
    happiness = response_specie['base_happiness']

    # capture rate
    capture_rate = response_specie['capture_rate']

    # base experience of pokemon, exp required at level 5
    exp = response['base_experience']

    embed.add_field(name="Name", value=name, inline=True)
    embed.add_field(name="ID", value=id, inline=True)
    embed.add_field(name="Weight", value=weight, inline=True)
    embed.add_field(name="Base Happiness", value=happiness, inline=True)
    embed.add_field(name="Capture Rate", value=capture_rate, inline=True)
    embed.add_field(name="Base Experience", value=exp, inline=True)

    embed.add_field(name="Type", value="==============================================", inline=False)

    # pokemon types
    types = response['types']

    type_counter = 1
    for type in types:
        embed.add_field(name="type" + str(type_counter), value=type['type']['name'], inline=True)
        type_counter += 1

    # getting the sprite of the pokemon
    sprite_front_url = response['sprites']['front_default']
    sprite_back_url = response['sprites']['back_default']
    print(sprite_back_url)
    print(sprite_front_url)

    # embed.set_image(url=sprite_front_url)
    embed.set_thumbnail(url=sprite_front_url)

    embed.add_field(name="Ablities", value="==============================================", inline=False)
    # pokemon abilities
    abilities = response['abilities']
    # getting the abilities name and is hidden or not
    ability_counter = 1
    for ability in abilities:
        print(ability)
        # getting the name of the ability
        print(ability['ability']['name'])
        # if the ability is hidden or not
        print("this ability is hidden: " + str(ability['is_hidden']))
        embed.add_field(name="ability"+str(ability_counter), value=ability['ability']['name'], inline=True)
        ability_counter += 1
    
    embed.add_field(name="Base Stats", value="==============================================", inline=False)
    # getting base stats of the pokemon
    stats = response['stats']
    for stat in stats:
        print('stat: ' + str(stat))
        print('base stat: ' + str(stat['base_stat']))
        print('stat json obj: ' + str(stat['stat']))
        print(stat['stat']['name'])
        embed.add_field(name=stat['stat']['name'], value=stat['base_stat'], inline=True)
    
    embed.add_field(name="Evolution", value="==============================================", inline=False)
    evolves_to = ''
    evolves_at_level = ''

    # print(response_specie['evolves_from_species'])
    # print(response_specie['varieties'][0]['pokemon']['name'])

    
    # getting moves
    moves = response['moves']
    embed.add_field(name="Moves", value="==============================================", inline=False)

    for move in moves:
        print(move)
        # print(move['move'])
        # name of the move
        # print(move['move']['name'])

        # getting the information above the move such as which version can the skill be learnt, how can it be learnt
        # print(move['version_group_details'])
        # what level is the move learned
        # print(move["version_group_details"][0]['level_learned_at'])
        # which game is it available
        # print(move['version_group_details'][0]['version_group']['name'])
        # how is the move learned
        # print(move['version_group_details'][0]['move_learn_method']['name'])
    
    return embed
        

# pokemon_basic_info('bulbasaur')

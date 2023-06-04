#########################################################################
#   File:        pokedex.py
#
#   Description: This file contains helper functions for pokemon
#                related commands. 
#                Pokemon is my childhood so it derserves a separate 
#                file for itself :)
#
#########################################################################


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
        title=response['name'],
        color=discord.Color.blurple()
    )

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


    # pokemon types
    types = response['types']
    # type list created so that I can use ",".join to avoid having to add a coma at the end of the whole string
    type_list = []
    for type in types:
        type_list.append(type['type']['name'])
        type_str = ", ".join(type_list)
    
    
    embed.add_field(name="Types\n=======================", value=type_str, inline=True)
    

    # getting the sprite of the pokemon
    sprite_front_url = response['sprites']['front_default']
    # sprite_back_url = response['sprites']['back_default']
    embed.set_thumbnail(url=sprite_front_url)

    # pokemon abilities
    abilities = response['abilities']
    # getting the abilities name and is hidden or not
    ability_list = []
    for ability in abilities:
        # getting the name of the ability
        ability_list.append(ability['ability']['name'])

    ability_str = ", ".join(ability_list)
    embed.add_field(name="Abilities\n=======================", value=ability_str, inline=True)
    

    # Pokemon base stat
    embed.add_field(name="Base Stats", value="**==============================================**", inline=False)
    # getting base stats of the pokemon
    stats = response['stats']
    for stat in stats:
        embed.add_field(name=stat['stat']['name'], value=stat['base_stat'], inline=True)
    
    embed.add_field(name="Evolution Chain", value="**==============================================**", inline=False)
    
    # pokemon evolution chain
    # getting evolution chain url 
    url_evolution_chain = response_specie['evolution_chain']['url']
    print(url_evolution_chain)
    response_evolution = requests.get(url_evolution_chain, headers={"Accept": "application/json"}).json()

    # getting first stage
    first_stage_name = response_evolution['chain']['species']['name']
    embed.add_field(name="First Stage", value=first_stage_name, inline=True)

    # getting the second stage evolution - stored in a list
    second_stage_list = response_evolution['chain']['evolves_to']
    second_stage = []
    second_stage_name = "null"
    if second_stage_list:
        for second_stage_item in second_stage_list:
            if "species" in second_stage_item:
                second_stage.append(second_stage_item['species']['name'])
        
        if len(second_stage) == 1:
            second_stage_name = second_stage[0]
        else:
            second_stage_name = ", ".join(second_stage)
    embed.add_field(name="Second Stage", value=second_stage_name, inline=True)

    # getting the third stage evolution
    third_stage_list = response_evolution['chain']['evolves_to']
    third_stage = []
    third_stage_name = "null"
    if third_stage_list:
        for third_stage_item in third_stage_list:
            if "evolves_to" in third_stage_item:
                print(len(third_stage))
                for evolves_to_item in third_stage_item['evolves_to']:
                    if "species" in evolves_to_item: 
                        print("inside if" + str(len(third_stage)))
                        third_stage.append(evolves_to_item['species']['name'])
        print("outside if" + str(len(third_stage)))
        if len(third_stage) == 0:
            third_stage_name = "null"
            # to prevent the else below from executing which would cause issues
            embed.add_field(name="Third Stage", value=third_stage_name, inline=True)
            return embed

        if len(third_stage) == 1:
            third_stage_name = third_stage[0]
        else:
            third_stage_name = ", ".join(third_stage)
    
    embed.add_field(name="Third Stage", value=third_stage_name, inline=True)

    return embed



    # individual ability info
    
    # Evolution
    # embed.add_field(name = chr(173), value = chr(173), inline=False)
    # embed.add_field(name="Evolution", value="==============================================", inline=False)
    # evolves_to = ''
    # evolves_at_level = ''
    # embed.add_field(name="Evolves From", value=response_specie['evolves_from_species'], inline=True)
    # embed.add_field(name="Evolves To", value=response_specie['varieties'][0]['pokemon']['name'], inline=True)
    # embed.add_field(name="place holder", value="place holder", inline=True)
    # print(response_specie['evolves_from_species'])
    # print(response_specie['varieties'][0]['pokemon']['name'])

    # information concerning an individual move
    
    # getting all moves of a pokemon
    # moves = response['moves']
    # embed.add_field(name="Moves", value="==============================================", inline=False)

    # for move in moves:
        # print(move)
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
    
        

# pokemon_basic_info('bulbasaur')
# def all_pokemon():
#     embed = discord.Embed(
#         title='All Pokemons',
#         color=discord.Color.blurple()
#     )
#     poke_list = ""
#     response = requests.get(url='https://pokeapi.co/api/v2/pokemon/?limit=10000', headers={"Accept": "application/json"}).json()
#     for pokemon in response['results']:
#         poke_list += pokemon['name'] + '\n'
    
#     # print(poke_list)
#     embed.add_field(name="pokemon", value=poke_list, inline=False)
#     return poke_list

# all_pokemon()

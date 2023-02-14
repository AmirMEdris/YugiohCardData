import json

# Opening JSON file
f = open('Yugioh/cardinfo.php')

# returns JSON object as
# a dictionary
data = json.load(f)

# Iterating through the json
# list

# data is a dict
print(type(data))
# printing data to see our dictionary
print(data)
'''
printing data seems to return the whole cardinfo file as a dict which is so big that if you check the begining of the output
it doesnt even line up with the begining of the actual file
the first thing in the actual file is the key data 
in my output the first thing is tcgplayer_price
'''
# jsons usually have nested structures of that switch back and forth using dictionaries and arrays of dictionaries
# so we need to get information about the data structure at each level to be able to use this data
# since we don't know the structure of our data dict we should first learn how many keys are on the outer most level
print(data.keys())
# .keys() returns a dict_keys() object which is baisically a list of keys present in this dictionary
# so we know everything in the outermost layer is in the key data
print(data['data'])
# its too long to tell in the output but data['data'] isnt itself a dictionary
print(type(data['data']))

# data is a list so lets get the first object in that list and see what it is
print(data['data'][0])

# data 0 is a dictionary that appears to contain the data for one card
# since now we have a list of dictionaries we should make a new variable
cardlist = data['data'][:]
# now we have an array of dicts where each dict is data for one card
print(len(cardlist))
# idk how many cards there should be but the length of this array is 12382 which sounds right to me

# accessing the dictionary keys in the first card
print(cardlist[0].keys())
# now we have more keys than before so imma just use a for loop to access all the data in this card

currentcard = cardlist[0]
for key in currentcard.keys():
    print(f"{key} = {currentcard[key]}")
# if you look at the output here some of the values are lists with one thing in them where the object is another
# dictionary like card_sets
# I feel that that will make accessing data more annoying than anything else so im going ad the values
# within dictionaries like that to the main card dictionary
# for example to access image url in card_images I have to do currentcard["card_images"][0]['image_url']
# instead I want to do currentcard["image_url"] to make life easier

for key in list(currentcard.keys()):
    if type(currentcard[key]) == list:
        for ckey in currentcard[key][0].keys():
            currentcard[ckey] = currentcard[key][0][ckey]

    print(f"{key} = {currentcard[key]}")

# show the new structure
for key in list(currentcard.keys()):
    print(f"{key} = {currentcard[key]}")


# now imma make that a function and do that for every card abd also delete the duplicate keys

def reformatcard(card):
    reformatedcard = card
    keys_to_delete = []
    for key in list(reformatedcard.keys()):
        if type(reformatedcard[key]) == list:
            if type(reformatedcard[key][0]) == str:
                continue
            for ckey in list(reformatedcard[key][0].keys()):
                reformatedcard[ckey] = reformatedcard[key][0][ckey]
            keys_to_delete.append(key)
    for dkey in keys_to_delete:
        del reformatedcard[dkey]

    return reformatedcard


CardIndex = dict()
for card in cardlist:
    cardid = card['id']
    rcard = reformatcard(card)
    CardIndex[cardid] = rcard
print(len(CardIndex.keys()))
print(CardIndex.keys())

# now you have a an index of cards you can use to get the dictionary for any card using id
print(CardIndex[34541863]['name'])

# Closing file
f.close()

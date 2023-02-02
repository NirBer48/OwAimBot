import os

def generate_negative_description_file():
    with open('neg.txt', 'w') as f:
        for filename in os.listdir('data//Negative'):
            f.write('data/Negative/' + filename + '\n')

generate_negative_description_file()
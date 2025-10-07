#Chat Bot V2
'''
Natural Language Understanding
- Understands Intent 
- Matches Intent and Descriptions to Response Templates
- Fills Response Template based on Intent and Descriptions
'''
import string
import spacy
import nltk
from nltk import word_tokenize, pos_tag
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
nltk.download('punkt')
nltk.download('wordnet')
import json
import random

class ChatBot:
    #Function: Get Data from Files
    def getData(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        return data

    #Function: Part-Of-Speech Tagging
    def POS_tagging(sentence):
        tokens = word_tokenize(sentence)
    
        pos_tags = pos_tag(tokens)

        nouns = []
        adjectives = []

        for word, pos in pos_tags:
            if pos.startswith('N'):
                nouns.append(word)
                adjectives.append(word)
            elif pos.startswith('J'): 
                adjectives.append(word)
        
        return nouns, adjectives

    #Function: Match nouns to intents
    def matchNounsToIntent(intents,nouns):
        maxMatchPattern = None
        maxMatchCount = None
        for intent in intents:
            curCount = 0
            pattern = intent["patterns"]
            for n in nouns:
                if n in pattern:
                    curCount += 1
            if maxMatchCount == None or curCount > maxMatchCount:
                maxMatchCount = curCount
                maxMatchPattern = intent["name"]

        if maxMatchPattern == None:
            return "Sorry, could you try rephrasing or rewording that?"
        return maxMatchPattern
    
    #Function: Match Adjectives to Genre/Description
    def matchDescriptions(genres,adjectives):
        maxMatchPattern = None
        maxMatchCount = None
        for genre in genres:
            curCount = 0
            pattern = genre["patterns"]
            for a in adjectives:
                if a in pattern:
                    curCount += 1
            if maxMatchCount == None or curCount > maxMatchCount:
                maxMatchCount = curCount
                maxMatchPattern = genre["name"]

        if maxMatchPattern == None:
            return "No Descriptions Found"
        return maxMatchPattern

    #Function: Find appropriate Response
    def getResponse(userMSG,intents,descriptions):
        userMSG = ChatBot.tokenize_stopwords(userMSG)
        pos = 0
        lemmatizer = WordNetLemmatizer()
        for i in userMSG:
            userMSG[pos] = userMSG[pos].lower()
            userMSG[pos] = lemmatizer.lemmatize(userMSG[pos])
            pos += 1
        
        stringFormMSG = ""
        for i in userMSG:
            stringFormMSG += i
            stringFormMSG += " "
        stringFormMSG = stringFormMSG.strip()
        nouns,adjectives = ChatBot.POS_tagging(stringFormMSG)

        foundIntent = ChatBot.matchNounsToIntent(intents,nouns)
        foundDescription = ChatBot.matchDescriptions(descriptions,adjectives)
        
        if foundIntent == "Sorry, could you try rephrasing or rewording that?":
            return foundIntent
        
        if foundIntent == "greeting" or foundIntent == "farewell":
            for intent in intents:
                if intent["name"] == foundIntent:
                    responses = intent["responses"]
                    break
            chosen = random.randint(0,len(responses)-1)
            return responses[chosen]

        for intent in intents:
            if intent["name"] == foundIntent:
                responses = intent["responses"]
                break

        chosen = random.randint(0,len(responses)-1)
        response = responses[chosen]
        response = response.replace("ADJ", foundDescription)


        for genre in descriptions:
            if genre["name"] == foundDescription:
                chosenGenre = genre["name"]
        
        movies = {
            "The Dark Knight": "action",
            "Inception": "action",
            "Pulp Fiction": "crime",
            "The Shawshank Redemption": "drama",
            "The Godfather": "crime",
            "The Matrix": "Science Fiction",
            "Forrest Gump": "drama",
            "Fight Club": "drama",
            "Titanic": "romance",
            "Jurassic Park": "adventure",
            "Ferris Bueller's Day Off": "comedy",
            "The Avengers": "action",
            "Interstellar": "Science Fiction",
            "The Lion King": "animation",
            "Gladiator": "action",
            "The Social Network": "drama",
            "The Departed": "crime",
            "The Prestige": "mystery",
            "The Lord of the Rings": "fantasy",
            "Casablanca": "romance",
            "The Silence of the Lambs": "thriller",
            "Inglourious Basterds": "war",
            "Back to the Future": "adventure",
            "The Notebook": "romance",
            "The Hangover": "comedy",
            "The Shining": "horror",
            "Eternal Sunshine of the Spotless Mind": "drama",
            "The Green Mile": "drama",
            "The Terminator": "Science Fiction",
            "The Princess Bride": "adventure",
            "Rocky": "drama",
            "The Dark Knight Rises": "action",
            "Scarface": "crime",
            "Jaws": "thriller",
            "Inferno": "mystery",
            "Avatar": "action",
            "The Sixth Sense": "thriller",
            "Die Hard": "action",
            "Gone with the Wind": "drama",
            "The Exorcist": "horror",
            "The Pursuit of Happyness": "drama",
            "The Bourne Identity": "action",
            "Harry Potter and the Philosopher's Stone": "fantasy",
            "The Notebook": "romance",
            "The Hangover": "comedy",
            "The Shining": "horror",
            "Eternal Sunshine of the Spotless Mind": "drama",
            "The Green Mile": "drama",
            "The Terminator": "Science Fiction",
            "The Princess Bride": "adventure",
            "Rocky": "drama",
            "The Dark Knight Rises": "action",
            "Scarface": "crime",
            "Jaws": "thriller",
            "Inferno": "mystery",
            "Avatar": "action",
            "The Sixth Sense": "thriller",
            "Die Hard": "action",
            "Gone with the Wind": "drama",
            "The Exorcist": "horror",
            "The Pursuit of Happyness": "drama",
            "The Bourne Identity": "action",
            "Harry Potter and the Philosopher's Stone": "fantasy",
            "The Notebook": "romance",
            "The Hangover": "comedy",
            "The Shining": "horror",
            "Eternal Sunshine of the Spotless Mind": "drama",
            "The Green Mile": "drama",
            "The Terminator": "Science Fiction",
            "The Princess Bride": "adventure",
            "Rocky": "drama",
            "The Dark Knight Rises": "action",
            "Scarface": "crime",
            "Jaws": "thriller",
            "Inferno": "mystery",
            "Avatar": "action",
            "The Sixth Sense": "thriller",
            "Die Hard": "action",
            "Gone with the Wind": "drama",
            "The Exorcist": "horror",
            "The Pursuit of Happyness": "drama",
            "The Bourne Identity": "action",
            "Harry Potter and the Philosopher's Stone": "fantasy",
            "The Notebook": "romance",
            "The Hangover": "comedy",
            "The Shining": "horror",
            "Eternal Sunshine of the Spotless Mind": "drama",
            "The Green Mile": "drama",
            "The Terminator": "Science Fiction",
            "The Princess Bride": "adventure",
            "Rocky": "drama",
            "The Dark Knight Rises": "action",
            "Scarface": "crime",
            "Jaws": "thriller",
            "Inferno": "mystery",
            "Avatar": "action",
            "The Sixth Sense": "thriller",
            "Die Hard": "action",
            "Gone with the Wind": "drama",
            "The Exorcist": "horror",
            "The Pursuit of Happyness": "drama",
            "The Bourne Identity": "action",
            "Harry Potter and the Philosopher's Stone": "fantasy",
            "The Notebook": "romance",
            "The Hangover": "comedy",
            "The Shining": "horror",
            "Eternal Sunshine of the Spotless Mind": "drama",
            "The Green Mile": "drama",
            "The Terminator": "Science Fiction",
            "The Princess Bride": "adventure",
            "Rocky": "drama",
            "The Dark Knight Rises": "action",
            "Scarface": "crime",
            "Jaws": "thriller",
            "Inferno": "mystery",
            "Avatar": "action",
            "The Sixth Sense": "thriller",
            "Die Hard": "action",
            "Gone with the Wind": "drama",
            "The Exorcist": "horror",
            "The Pursuit of Happyness": "drama",
            "The Bourne Identity": "action",
            "Harry Potter and the Philosopher's Stone": "fantasy",
            "The Notebook": "romance",
            "The Hangover": "comedy",
            "The Shining": "horror",
            "Eternal Sunshine of the Spotless Mind": "drama",
            "The Green Mile": "drama",
            "The Terminator": "Science Fiction",
            "The Princess Bride": "adventure",
            "Rocky": "drama",
            "The Dark Knight Rises": "action",
            "Scarface": "crime",
            "Jaws": "thriller",
            "Inferno": "mystery",
            "Avatar": "action",
            "The Sixth Sense": "thriller",
            "Die Hard": "action",
            "Gone with the Wind": "drama",
            "The Exorcist": "horror",
            "The Pursuit of Happyness": "drama",
            "The Bourne Identity": "action",
            "Harry Potter and the Philosopher's Stone": "fantasy"
        }
        
        books = {
            "To Kill a Mockingbird": "Classic",
            "1984": "Dystopian",
            "The Great Gatsby": "Classic",
            "The Catcher in the Rye": "Coming-of-Age",
            "Pride and Prejudice": "Romance",
            "Harry Potter and the Sorcerer's Stone": "Fantasy",
            "The Lord of the Rings": "Fantasy",
            "Gone Girl": "Mystery",
            "The Hunger Games": "Dystopian",
            "The Da Vinci Code": "Thriller",
            "Brave New World": "Dystopian",
            "The Adventures of Sherlock Holmes": "Mystery",
            "The Kite Runner": "Drama",
            "The Help": "Historical Fiction",
            "The Giver": "Dystopian",
            "The Maze Runner": "Dystopian",
            "The Fault in Our Stars": "Young Adult",
            "The Girl with the Dragon Tattoo": "Crime",
            "To Kill a Mockingbird": "Classic",
            "1984": "Dystopian",
            "The Catcher in the Rye": "Coming-of-Age",
            "Pride and Prejudice": "Romance",
            "Harry Potter and the Sorcerer's Stone": "Fantasy",
            "The Lord of the Rings": "Fantasy",
            "Gone Girl": "Mystery",
            "The Hunger Games": "Dystopian",
            "The Da Vinci Code": "Thriller",
            "Brave New World": "Dystopian",
            "Animal Farm": "Satire",
            "The Adventures of Sherlock Holmes": "Mystery",
            "The Kite Runner": "Drama",
            "The Help": "Historical Fiction",
            "The Giver": "Dystopian",
            "The Maze Runner": "Dystopian",
            "The Fault in Our Stars": "Young Adult",
            "The Girl with the Dragon Tattoo": "Crime",
            "The Picture of Dorian Gray": "Horror",
            "The Alchemist": "Fantasy",
            "Little Women": "Classic",
            "Frankenstein": "Horror",
            "The Chronicles of Narnia": "Fantasy",
            "The Hobbit": "Fantasy",
            "A Tale of Two Cities": "Historical Fiction",
            "Moby-Dick": "Adventure",
            "The Odyssey": "Classic",
            "The Count of Monte Cristo": "Adventure",
            "The Scarlet Letter": "Historical Fiction",
            "The Brothers Karamazov": "Philosophical Fiction",
            "The Adventures of Huckleberry Finn": "Adventure",
            "War and Peace": "Historical Fiction",
            "Sense and Sensibility": "Romance",
            "The Old Man and the Sea": "Adventure",
            "Les Misérables": "Historical Fiction",
            "The Bell Jar": "Biography",
            "The Alchemist": "Fantasy",
            "Little Women": "Classic",
            "The Chronicles of Narnia": "Fantasy",
            "The Hobbit": "Fantasy",
            "A Tale of Two Cities": "Historical Fiction",
            "Moby-Dick": "Adventure",
            "The Count of Monte Cristo": "Adventure",
            "The Scarlet Letter": "Historical Fiction",
            "The Adventures of Huckleberry Finn": "Adventure",
            "War and Peace": "Historical Fiction",
            "Sense and Sensibility": "Romance",
            "The Old Man and the Sea": "Adventure",
            "Les Misérables": "Historical Fiction",
            "The Bell Jar": "Biography"
        }

        games = {
            "Assassin's Creed Valhalla": "Action",
            "The Legend of Zelda: Breath of the Wild": "Adventure",
            "The Witcher 3: Wild Hunt": "Role-Playing",
            "Civilization VI": "Strategy",
            "The Sims 4": "Simulation",
            "FIFA 21": "Sports",
            "Mario Kart 8 Deluxe": "Racing",
            "Super Mario Odyssey": "Platformer",
            "Call of Duty: Modern Warfare": "First-Person Shooter",
            "Minecraft": "Sandbox",
            "Beat Saber": "Virtual Reality",
            "Subnautica": "Survival",
            "Portal 2": "Puzzle",
            "Rocket League": "Sports",
            "Red Dead Redemption 2": "Action",
            "Fallout 4": "Role-Playing",
            "Battlefield V": "First-Person Shooter",
            "Grand Theft Auto V": "Action",
            "Farming Simulator 19": "Simulation",
            "Super Smash Bros. Ultimate": "Fighting",
            "Overwatch": "First-Person Shooter",
            "NBA 2K21": "Sports",
            "Fortnite": "Battle Royale",
            "Cities: Skylines": "Simulation",
            "Resident Evil Village": "Survival",
            "Pokémon Sword and Shield": "Role-Playing",
            "Far Cry 5": "Action",
            "Tom Clancy's Rainbow Six Siege": "First-Person Shooter",
            "Stardew Valley": "Simulation",
            "The Elder Scrolls V: Skyrim": "Role-Playing",
            "Star Wars Jedi: Fallen Order": "Action",
            "Cuphead": "Platformer",
            "Dead by Daylight": "Survival",
            "F1 2020": "Racing",
            "The Last of Us Part II": "Adventure",
            "Gears 5": "Action",
            "No Man's Sky": "Adventure",
            "Fire Emblem: Three Houses": "Role-Playing",
            "Sekiro: Shadows Die Twice": "Action",
            "Planet Coaster": "Simulation",
            "Doom Eternal": "First-Person Shooter",
            "Animal Crossing: New Horizons": "Simulation",
            "Mortal Kombat 11": "Fighting",
            "Diablo III": "Role-Playing",
            "Forza Horizon 4": "Racing",
            "Hades": "Action",
            "Football Manager 2021": "Sports",
            "The Outer Worlds": "Role-Playing",
            "Among Us": "Strategy",
            "Ghost of Tsushima": "Action-Adventure",
            "Horizon Zero Dawn": "Action-Adventure",
            "Rainbow Six Siege": "First-Person Shooter",
            "SimCity": "Simulation",
            "Super Mario Maker 2": "Platformer",
            "Assassin's Creed Odyssey": "Action",
            "Borderlands 3": "Action",
            "Need for Speed Heat": "Racing",
            "Superhot": "First-Person Shooter",
            "The Legend of Zelda: Link's Awakening": "Adventure",
            "Civilization V": "Strategy",
            "NHL 21": "Sports",
            "Watch Dogs: Legion": "Action-Adventure",
            "Madden NFL 21": "Sports",
            "Resident Evil 3": "Survival Horror",
            "Final Fantasy VII Remake": "Role-Playing",
            "Minecraft Dungeons": "Action",
            "Crash Bandicoot 4: It's About Time": "Platformer",
            "Splatoon 2": "Third-Person Shooter",
            "Control": "Action-Adventure",
            "Destiny 2": "First-Person Shooter",
            "Civilization IV": "Strategy",
            "Assassin's Creed Origins": "Action",
            "Half-Life: Alyx": "Virtual Reality",
            "Dying Light": "Action",
            "Euro Truck Simulator 2": "Simulation",
            "Kingdom Hearts III": "Action Role-Playing",
            "Rise of the Tomb Raider": "Action-Adventure",
            "StarCraft II": "Strategy",
            "Batman: Arkham Knight": "Action",
            "Ori and the Will of the Wisps": "Platformer",
            "Sniper Elite 4": "Shooter",
            "Warhammer: Vermintide 2": "Action",
            "Darksiders III": "Action-Adventure",
            "The Division 2": "Action Role-Playing",
            "Slay the Spire": "Card Game",
            "Halo: The Master Chief Collection": "First-Person Shooter",
            "For Honor": "Action",
            "Mafia: Definitive Edition": "Action-Adventure",
            "Resident Evil 7: Biohazard": "Survival Horror",
            "Little Nightmares II": "Adventure",
            "DOOM (2016)": "First-Person Shooter",
            "Fallout: New Vegas": "Role-Playing",
            "Terraria": "Sandbox",
            "Planet Zoo": "Simulation",
            "RimWorld": "Simulation",
            "Ghostrunner": "Action",
            "Divinity: Original Sin II": "Role-Playing",
            "Uncharted 4: A Thief's End": "Action-Adventure",
            "Genshin Impact": "Action Role-Playing",
            "Crusader Kings III": "Strategy",
            "Devil May Cry 5": "Action",
            "Resident Evil 2 (2019)": "Survival Horror",
            "The Witness": "Puzzle",
            "Watch Dogs 2": "Action-Adventure",
            "Star Wars Battlefront II": "First-Person Shooter",
            "Darkest Dungeon": "Role-Playing",
            "Tropico 6": "Strategy",
            "Outlast": "Survival Horror",
            "Dead Cells": "Action",
            "Ghost Recon Breakpoint": "Action",
            "Sea of Thieves": "Adventure",
            "Anno 1800": "Strategy",
            "Diablo II": "Role-Playing",
            "Detroit: Become Human": "Interactive Drama",
            "Tom Clancy's The Division": "Action Role-Playing",
            "XCOM 2": "Strategy",
            "Pokémon: Let's Go, Pikachu! and Let's Go, Eevee!": "Role-Playing",
            "Dragon Age: Inquisition": "Role-Playing",
            "Metal Gear Solid V: The Phantom Pain": "Action-Adventure",
            "Monster Hunter: World": "Action Role-Playing",
            "Bioshock Infinite": "First-Person Shooter"
        }
        music = {
            "Shape of You": "Pop",
            "Bohemian Rhapsody": "Rock",
            "Humble": "Hip Hop",
            "Take Five": "Jazz",
            "Für Elise": "Classical",
            "Enter Sandman": "Metal",
            "The Times They Are a-Changin'": "Folk",
            "Rolling in the Deep": "Pop",
            "Hotel California": "Rock",
            "Juicy": "Hip Hop",
            "Fly Me to the Moon": "Jazz",
            "Moonlight Sonata": "Classical",
            "Master of Puppets": "Metal",
            "Blowin' in the Wind": "Folk",
            "Billie Jean": "Pop",
            "Stairway to Heaven": "Rock",
            "Empire State of Mind": "Hip Hop",
            "Take the 'A' Train": "Jazz",
            "Canon in D": "Classical",
            "Paranoid": "Metal",
            "The Sound of Silence": "Folk",
            "Thinking Out Loud": "Pop",
            "Smells Like Teen Spirit": "Rock",
            "Lose Yourself": "Hip Hop",
            "Summertime": "Jazz",
            "Symphony No. 5": "Classical",
            "Numb": "Metal",
            "Mr. Tambourine Man": "Folk",
            "All of Me": "Pop",
            "Wonderwall": "Rock",
            "Stan": "Hip Hop",
            "My Favorite Things": "Jazz",
            "Fur Alina": "Classical",
            "One": "Metal",
            "Blowin' in the Wind": "Folk",
            "Don't Start Now": "Pop",
            "Smells Like Teen Spirit": "Rock",
            "Hotline Bling": "Hip Hop",
            "Take the 'A' Train": "Jazz",
            "Rhapsody in Blue": "Classical",
            "Enter Sandman": "Metal",
            "The Sound of Silence": "Folk",
            "Bad Guy": "Pop",
            "Highway to Hell": "Rock",
            "Lose Yourself": "Hip Hop",
            "Blue Bossa": "Jazz",
            "Canon in D": "Classical",
            "Master of Puppets": "Metal",
            "Blowin' in the Wind": "Folk",
            "Someone Like You": "Pop",
            "Sweet Child o' Mine": "Rock",
            "99 Problems": "Hip Hop",
            "Fly Me to the Moon": "Jazz",
            "Für Elise": "Classical",
            "Paranoid": "Metal",
            "Blowin' in the Wind": "Folk",
            "Love Yourself": "Pop",
            "Hotel California": "Rock",
            "Empire State of Mind": "Hip Hop",
            "Take Five": "Jazz",
            "Moonlight Sonata": "Classical",
            "Enter Sandman": "Metal",
            "The Sound of Silence": "Folk",
            "Shape of You": "Pop",
            "Bohemian Rhapsody": "Rock",
            "Juicy": "Hip Hop",
            "Summertime": "Jazz",
            "Für Elise": "Classical",
            "Numb": "Metal",
            "Mr. Tambourine Man": "Folk",
            "Rolling in the Deep": "Pop",
            "Hotel California": "Rock",
            "Lose Yourself": "Hip Hop",
            "Take Five": "Jazz",
            "Canon in D": "Classical",
            "Master of Puppets": "Metal",
            "Blowin' in the Wind": "Folk",
            "Thinking Out Loud": "Pop",
            "Smells Like Teen Spirit": "Rock",
            "Humble": "Hip Hop",
            "Fly Me to the Moon": "Jazz",
            "Moonlight Sonata": "Classical",
            "Enter Sandman": "Metal",
            "The Times They Are a-Changin'": "Folk",
            "Billie Jean": "Pop",
            "Stairway to Heaven": "Rock",
            "Juicy": "Hip Hop",
            "Take the 'A' Train": "Jazz",
            "Canon in D": "Classical",
            "Paranoid": "Metal",
            "The Sound of Silence": "Folk",
            "Thinking Out Loud": "Pop",
            "Smells Like Teen Spirit": "Rock",
            "Lose Yourself": "Hip Hop",
            "Take Five": "Jazz",
            "Symphony No. 5": "Classical",
            "Numb": "Metal",
            "Mr. Tambourine Man": "Folk",
            "All of Me": "Pop",
            "Wonderwall": "Rock",
            "Stan": "Hip Hop",
            "My Favorite Things": "Jazz",
            "Fur Alina": "Classical",
            "One": "Metal",
            "Blowin' in the Wind": "Folk",
            "Don't Start Now": "Pop",
            "Smells Like Teen Spirit": "Rock",
            "Hotline Bling": "Hip Hop",
            "Take the 'A' Train": "Jazz",
            "Rhapsody in Blue": "Classical",
            "Enter Sandman": "Metal",
            "The Sound of Silence": "Folk",
            "Bad Guy": "Pop",
            "Highway to Hell": "Rock",
            "Lose Yourself": "Hip Hop",
            "Blue Bossa": "Jazz",
            "Canon in D": "Classical",
            "Master of Puppets": "Metal",
            "Blowin' in the Wind": "Folk",
            "Someone Like You": "Pop",
            "Sweet Child o' Mine": "Rock",
            "99 Problems": "Hip Hop",
            "Fly Me to the Moon": "Jazz",
            "Für Elise": "Classical",
            "Paranoid": "Metal",
            "Blowin' in the Wind": "Folk",
            "Love Yourself": "Pop",
            "Hotel California": "Rock",
            "Empire State of Mind": "Hip Hop",
            "Take Five": "Jazz",
            "Moonlight Sonata": "Classical",
            "Enter Sandman": "Metal",
            "The Sound of Silence": "Folk"
        }

        tv_shows = {
            "Friends": "Comedy",
            "Breaking Bad": "Drama",
            "Stranger Things": "Science Fiction",
            "Game of Thrones": "Fantasy",
            "The Office": "Comedy",
            "The Crown": "Drama",
            "Black Mirror": "Science Fiction",
            "The Big Bang Theory": "Comedy",
            "Sherlock": "Mystery",
            "The Walking Dead": "Horror",
            "Fargo": "Crime",
            "Mindhunter": "Crime",
            "Westworld": "Science Fiction",
            "Better Call Saul": "Drama",
            "The Witcher": "Fantasy",
            "The Mandalorian": "Science Fiction",
            "Breaking Bad": "Drama",
            "Narcos": "Crime",
            "True Detective": "Crime",
            "Peaky Blinders": "Drama",
            "Money Heist": "Crime",
            "Ozark": "Drama",
            "Homeland": "Thriller",
            "Chernobyl": "Drama",
            "Lost": "Adventure",
            "Stranger Things": "Science Fiction",
            "The Office": "Comedy",
            "The Crown": "Drama",
            "Black Mirror": "Science Fiction",
            "Sherlock": "Mystery",
            "The Handmaid's Tale": "Drama",
            "The Big Bang Theory": "Comedy",
            "Friends": "Comedy",
            "Game of Thrones": "Fantasy",
            "Breaking Bad": "Drama",
            "The Walking Dead": "Horror",
            "The Sopranos": "Crime",
            "House of Cards": "Drama",
            "Dexter": "Crime",
            "Vikings": "Action",
            "Stranger Things": "Science Fiction",
            "Prison Break": "Action",
            "How I Met Your Mother": "Comedy",
            "The Simpsons": "Animation",
            "True Blood": "Fantasy",
            "The Blacklist": "Crime",
            "Orange Is the New Black": "Drama",
            "The Wire": "Crime",
            "Westworld": "Science Fiction",
            "Sherlock": "Mystery",
            "The Mandalorian": "Science Fiction",
            "Friends": "Comedy",
            "Breaking Bad": "Drama",
            "Stranger Things": "Science Fiction",
            "Game of Thrones": "Fantasy",
            "The Office": "Comedy",
            "The Crown": "Drama",
            "Black Mirror": "Science Fiction",
            "The Big Bang Theory": "Comedy",
            "Sherlock": "Mystery",
            "The Walking Dead": "Horror",
            "Fargo": "Crime",
            "Mindhunter": "Crime",
            "Westworld": "Science Fiction",
            "Better Call Saul": "Drama",
            "The Witcher": "Fantasy",
            "The Mandalorian": "Science Fiction",
            "Breaking Bad": "Drama",
            "Narcos": "Crime",
            "True Detective": "Crime",
            "Peaky Blinders": "Drama",
            "Money Heist": "Crime",
            "Ozark": "Drama",
            "Homeland": "Thriller",
            "Chernobyl": "Drama",
            "Lost": "Adventure",
            "Stranger Things": "Science Fiction",
            "The Office": "Comedy",
            "The Crown": "Drama",
            "Black Mirror": "Science Fiction",
            "Sherlock": "Mystery",
            "The Handmaid's Tale": "Drama",
            "The Big Bang Theory": "Comedy",
            "Friends": "Comedy",
            "Game of Thrones": "Fantasy",
            "Breaking Bad": "Drama",
            "The Walking Dead": "Horror",
            "The Sopranos": "Crime",
            "House of Cards": "Drama",
            "Dexter": "Crime",
            "Vikings": "Action",
            "Stranger Things": "Science Fiction",
            "Prison Break": "Action",
            "How I Met Your Mother": "Comedy",
            "The Simpsons": "Animation",
            "True Blood": "Fantasy",
            "The Blacklist": "Crime",
            "Orange Is the New Black": "Drama",
            "The Wire": "Crime",
            "Westworld": "Science Fiction",
            "Sherlock": "Mystery",
            "The Mandalorian": "Science Fiction",
            "Friends": "Comedy",
            "Breaking Bad": "Drama",
            "Stranger Things": "Science Fiction",
            "Game of Thrones": "Fantasy",
            "The Office": "Comedy",
            "The Crown": "Drama",
            "Black Mirror": "Science Fiction",
            "The Big Bang Theory": "Comedy",
            "Sherlock": "Mystery",
            "The Walking Dead": "Horror",
            "Fargo": "Crime",
            "Mindhunter": "Crime",
            "Westworld": "Science Fiction",
            "Better Call Saul": "Drama",
            "The Witcher": "Fantasy",
            "The Mandalorian": "Science Fiction",
            "Breaking Bad": "Drama",
            "Narcos": "Crime",
            "True Detective": "Crime",
            "Peaky Blinders": "Drama",
            "Money Heist": "Crime",
            "Ozark": "Drama",
            "Homeland": "Thriller",
            "Chernobyl": "Drama",
            "Lost": "Adventure",
            "Stranger Things": "Science Fiction",
            "The Office": "Comedy",
            "The Crown": "Drama",
            "Black Mirror": "Science Fiction",
            "Sherlock": "Mystery",
            "The Handmaid's Tale": "Drama",
            "The Big Bang Theory": "Comedy",
            "Friends": "Comedy",
            "Game of Thrones": "Fantasy",
            "Breaking Bad": "Drama",
            "The Walking Dead": "Horror",
            "The Sopranos": "Crime",
            "House of Cards": "Drama",
            "Dexter": "Crime",
            "Vikings": "Action",
            "Stranger Things": "Science Fiction",
            "Prison Break": "Action",
            "How I Met Your Mother": "Comedy",
            "The Simpsons": "Animation",
            "True Blood": "Fantasy",
            "The Blacklist": "Crime",
            "Orange Is the New Black": "Drama",
            "The Wire": "Crime",
            "Westworld": "Science Fiction",
            "Sherlock": "Mystery",
            "The Mandalorian": "Science Fiction",
            "Friends": "Comedy",
            "Breaking Bad": "Drama",
            "Stranger Things": "Science Fiction",
            "Game of Thrones": "Fantasy",
            "The Office": "Comedy",
            "The Crown": "Drama",
            "Black Mirror": "Science Fiction",
            "The Big Bang Theory": "Comedy",
            "Sherlock": "Mystery",
            "The Walking Dead": "Horror",
            "Fargo": "Crime",
            "Mindhunter": "Crime",
            "Westworld": "Science Fiction",
            "Better Call Saul": "Drama",
            "The Witcher": "Fantasy",
            "The Mandalorian": "Science Fiction",
            "Breaking Bad": "Drama",
            "Narcos": "Crime",
            "True Detective": "Crime",
            "Peaky Blinders": "Drama",
            "Money Heist": "Crime",
            "Ozark": "Drama",
            "Homeland": "Thriller",
            "Chernobyl": "Drama",
            "Lost": "Adventure",
            "Stranger Things": "Science Fiction",
            "The Office": "Comedy",
            "The Crown": "Drama",
            "Black Mirror": "Science Fiction",
            "Sherlock": "Mystery",
            "The Handmaid's Tale": "Drama",
            "The Big Bang Theory": "Comedy",
            "Friends": "Comedy",
            "Game of Thrones": "Fantasy",
            "Breaking Bad": "Drama",
            "The Walking Dead": "Horror",
            "The Sopranos": "Crime",
            "House of Cards": "Drama",
            "Dexter": "Crime",
            "Vikings": "Action",
            "Stranger Things": "Science Fiction",
            "Prison Break": "Action",
            "How I Met Your Mother": "Comedy",
            "The Simpsons": "Animation",
            "True Blood": "Fantasy",
            "The Blacklist": "Crime",
            "Orange Is the New Black": "Drama",
            "The Wire": "Crime",
            "Westworld": "Science Fiction",
            "Sherlock": "Mystery",
            "The Mandalorian": "Science Fiction",
            "Friends": "Comedy",
            "Breaking Bad": "Drama",
            "Stranger Things": "Science Fiction",
            "Game of Thrones": "Fantasy",
            "The Office": "Comedy",
            "The Crown": "Drama",
            "Black Mirror": "Science Fiction",
            "The Big Bang Theory": "Comedy",
            "Sherlock": "Mystery",
            "The Walking Dead": "Horror",
            "Fargo": "Crime",
            "Mindhunter": "Crime",
            "Westworld": "Science Fiction",
            "Better Call Saul": "Drama",
            "The Witcher": "Fantasy",
            "The Mandalorian": "Science Fiction",
            "Breaking Bad": "Drama",
            "Narcos": "Crime",
            "True Detective": "Crime",
            "Peaky Blinders": "Drama",
            "Money Heist": "Crime",
            "Ozark": "Drama",
            "Homeland": "Thriller",
            "Chernobyl": "Drama",
            "Lost": "Adventure",
            "Stranger Things": "Science Fiction",
            "The Office": "Comedy",
            "The Crown": "Drama",
            "Black Mirror": "Science Fiction",
            "Sherlock": "Mystery",
            "The Handmaid's Tale": "Drama",
            "The Big Bang Theory": "Comedy",
            "Friends": "Comedy",
            "Game of Thrones": "Fantasy",
            "Breaking Bad": "Drama",
            "The Walking Dead": "Horror",
            "The Sopranos": "Crime"
        }
    

        recommendations = []
        if foundIntent == "movie_recommendation":
            for i in movies:
                if movies[i].lower() == chosenGenre.lower():
                    recommendations.append(i)
        elif foundIntent == "book_recommendation":
            for i in books:
                if books[i].lower() == chosenGenre.lower():
                    recommendations.append(i)
        elif foundIntent == "game_recommendation":
            for i in games:
                if games[i].lower() == chosenGenre.lower():
                    recommendations.append(i)
        elif foundIntent == "music_recommendation":
            for i in music:
                if music[i].lower() == chosenGenre.lower():
                    recommendations.append(i)
        elif foundIntent == "tv_show_recommendation":
            for i in tv_shows:
                if tv_shows[i].lower() == chosenGenre.lower():
                    recommendations.append(i)
        

        chosen = random.randint(0,len(recommendations)-1)
        recommendation = recommendations[chosen]


        response = response.replace("RECOM",recommendation)
        response = response.replace("{","")
        response = response.replace("}","")

        return response
        
        


        
        


        

    #Function: Tokenize User Message and Remove Stop Words
    def tokenize_stopwords(message):
        message = message.translate(str.maketrans('', '', string.punctuation))
        message = message.split()

        pos = 0
        stop_words = ChatBot.getStopWords()

        while pos < len(message):
            if len(message) == 0 or pos>= len(message):break
            if message[pos] in stop_words:
                del(message[pos])
            else:
                pos += 1
        return message
            

    #Function: Read Stop Words from File
    def getStopWords():
        r = open("stop_words","r")
        stop_words = set()
        while len(stop_words) < 162:
            word = r.readline()
            word = word.strip()
            stop_words.add(word)
        return stop_words


    #Function: main
    def init():
        print("Starting Conversation:")
        knowledge = ChatBot.getData("ChatBotV3ProcessingData.json")
        intents = knowledge["intents"]
        description = knowledge["genres"]
        while True:
            userMSG = str(input())
            userMSG = userMSG.strip()
            if userMSG == "2023":
                print("Quitting")
                break

            print(ChatBot.getResponse(userMSG,intents,description))
            

        return


ChatBot.init()

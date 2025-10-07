#Chat Bot V4
'''
Natural Language Understanding
- Understands Intent 
- Matches Intent and Descriptions to Response Templates
- Fills Response Template based on Intent and Descriptions
 
Basic Reinforcement Learning
- Learns User Preferences and Dislikes 
- Tracks reward/score system by genre
- Can fill in gaps in user input using user data and preferences. 
'''

import string
import nltk
from nltk import word_tokenize, pos_tag
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import random


class ChatBot:
    def init():
        print("Starting Conversation")
        probabilityDistribution = {
            "Action": 0.025,
            "Adventure": 0.025,
            "Animation": 0.025,
            "Comedy": 0.025,
            "Crime": 0.025,
            "Documentary": 0.025,
            "Drama": 0.025,
            "Family": 0.025,
            "Fantasy": 0.025,
            "Horror": 0.025,
            "Musical": 0.025,
            "Mystery": 0.025,
            "Romance": 0.025,
            "Sci-Fi": 0.025,
            "Thriller": 0.025,
            "Western": 0.025,
            "Biography": 0.025,
            "Historical": 0.025,
            "War": 0.025,
            "Sports": 0.025,
            "Supernatural": 0.025,
            "Suspense": 0.025,
            "Noir": 0.025,
            "Psychological": 0.025,
            "Satire": 0.025,
            "Coming-of-Age": 0.025,
            "Rock": 0.025,
            "Pop": 0.025,
            "Hip Hop": 0.025,
            "Jazz": 0.025,
            "Country": 0.025,
            "Classical": 0.025,
            "Reggae": 0.025,
            "R&B": 0.025,
            "Electronic": 0.025,
            "Folk": 0.025,
            "Indie": 0.025,
            "Metal": 0.025,
            "Punk": 0.025,
            "Blues": 0.025
        }

        rewards = {}
        prevGenres = ""
        while True:
            userMSG = str(input())
            userMSG = userMSG.strip()
            if userMSG == "Show":
                print(probabilityDistribution)
                continue
            botResponse, usedGenre = ChatBot.getResponse(userMSG,probabilityDistribution)
            if botResponse != "feedback message":
                print(botResponse)
            else:
                feedbackDict = {
                    "positiveFeedback": "positive",
                    "negativeFeedback": "negative"
                }
                probabilityDistribution = ChatBot.updateProbabilityDistribution(probabilityDistribution,prevGenre,feedbackDict[usedGenre])
                if usedGenre == "positiveFeedback":
                    print("Great! I'm glad you enjoyed it.")
                else:
                    print("Sorry about that. Feel free to ask for another suggestion!")

            prevGenre = usedGenre
            botResponse = ""
            usedGenre = ""

    def getResponse(userMSG,probabilityDistribution):
        userMSG = ChatBot.tokenize(userMSG)
        lemmatizer = WordNetLemmatizer()
        pos = 0
        for i in userMSG:
            userMSG[pos] = userMSG[pos].lower()
            userMSG[pos] = lemmatizer.lemmatize(userMSG[pos])
            pos += 1 

        stringFormMSG = ""
        for i in userMSG:
            stringFormMSG += i
            stringFormMSG += " "
        stringFormMSG = stringFormMSG.strip()
        nouns,adjectives = ChatBot.part_of_speech_tagging(stringFormMSG)

        entertainmentType = ChatBot.getEntertainmentType(nouns)
        genre = ChatBot.getGenre(adjectives+nouns) 
        if entertainmentType == "positiveFeedback":
            return "feedback message", "positiveFeedback"
        elif entertainmentType == "negativeFeedback":
            return "feedback message", "negativeFeedback"

        if genre != "any" and entertainmentType != "any":
            recommendation = ChatBot.findEntertainment(entertainmentType, genre.lower())
            if recommendation == "Not Found":
                return "Sorry, I couldn't find a recommendation like that. Can you try something else?"
            sentence = ChatBot.responseSentence(recommendation,genre)
            return sentence, genre
        elif genre != "any" and entertainmentType == "any":
            entertainmentOptions = ["movie","book","music","tv show","game"]
            possibleRecommendations = []
            for e in entertainmentOptions:
                possibleRecommendation = ChatBot.findEntertainment(e,genre.lower())
                if possibleRecommendation != "Not Found":
                    possibleRecommendations.append(possibleRecommendation)
            if possibleRecommendations == []:
                return "Sorry, I couldn't find a recommendation like that. Can you try something else?"
            sentence = ChatBot.responseSentence(possibleRecommendations[random.randint(0,len(possibleRecommendations)-1)],genre.lower()) 
            return sentence, genre

        elif genre == "any" and entertainmentType != "any":
            genre = ChatBot.suggestGenre(probabilityDistribution)
            recommendation = ChatBot.findEntertainment(entertainmentType,genre.lower())
            done = 0
            while recommendation == "Not Found" and done < 100:
                genre = ChatBot.suggestGenre(probabilityDistribution)
                recommendation = ChatBot.findEntertainment(entertainmentType,genre.lower())
                done += 1
            if recommendation == "Not Found":
                return "Sorry, I couldn't find a recommendation for you. You can try asking for a different suggestion."

            sentence = ChatBot.responseSentence(recommendation,genre.lower())
            return sentence, genre
        else:
            genre = ChatBot.suggestGenre(probabilityDistribution)
            entertainmentOptions = ["movie","book","music","tv show","game"]
            possibleRecommendations = []
            for e in entertainmentOptions:
                recommendation = ChatBot.findEntertainment(e,genre.lower())
                if recommendation != "Not Found":
                    possibleRecommendations.append(recommendation)
            
            sentence = ChatBot.responseSentence(possibleRecommendations[random.randint(0,len(possibleRecommendations)-1)],genre)
            return sentence, genre

    def updateProbabilityDistribution(probabilityDistribution, genre, feedback):
        updatedDistribution = probabilityDistribution.copy()

        if genre in updatedDistribution:
            
            if feedback == 'positive':
                updatedDistribution[genre] += 0.025  
            elif feedback == 'negative':
                updatedDistribution[genre] -= 0.025 
            
            updatedDistribution[genre] = max(0, min(1, updatedDistribution[genre]))
        else:
            # If the genre is not in the distribution, add it with an initial probability
            if feedback == 'positive':
                updatedDistribution[genre] = 0.1  # Set initial probability to 0.1
            elif feedback == 'negative':
                updatedDistribution[genre] = 0.0  # Set initial probability to 0.0
        
        # Normalize the probabilities to ensure they add up to 1
        totalProbability = sum(updatedDistribution.values())
        if totalProbability > 0:
            for genre in updatedDistribution:
                updatedDistribution[genre] /= totalProbability
        
        return updatedDistribution

    def suggestGenre(probabilityDistribution):
        # Get the genres and their corresponding probabilities
        genres = list(probabilityDistribution.keys())
        probabilities = list(probabilityDistribution.values())

        # Choose a genre based on the probability distribution
        chosenGenre = random.choices(genres, probabilities)[0]
        
        return chosenGenre

    def getEntertainmentType(nouns):
        entertainment_keywords = {
            "movie": ["film", "cinema", "movie", "actor", "actress", "director", "plot", "trailer"],
            "book": ["book", "novel", "author", "chapter", "fiction", "non-fiction", "reading"],
            "music": ["music", "song", "artist", "album", "genre", "lyrics", "melody","listen"],
            "tv show": ["tv show", "series", "episode", "season", "cast", "character", "plot twist"],
            "game": ["game", "game", "gaming", "console", "multiplayer", "strategy","fps","role-play, rpg"],
            "positiveFeedback": ["thank","thanks","great","good","love","wow","nice","brilliant","amazing"],
            "negativeFeedback": ["bad","terrible","else","didnt","dont","wont","hate","boring","annoying"]
            # Add more entertainment types and their corresponding keywords
        }
        maxMatches = 0
        maxMatched = None
        for t in entertainment_keywords:
            numMatches = 0
            for n in nouns:
                if n in entertainment_keywords[t]:
                    numMatches += 1
            if numMatches > maxMatches:
                maxMatches = numMatches
                maxMatched = t
        
        if not maxMatched:
            return "any"
        return maxMatched
    
    def getGenre(adjectives):
        genre_adjectives = {
            "Action": ["thrilling", "explosive", "intense", "adrenaline-pumping", "action-packed", "action"],
            "Adventure": ["exciting", "daring", "epic", "journey-filled", "thrilling", "adventure"],
            "Animation": ["animated", "colorful", "imaginative", "whimsical", "charming", "animation"],
            "Comedy": ["funny", "hilarious", "humorous", "entertaining", "lighthearted", "comedy"],
            "Crime": ["suspenseful", "gritty", "intriguing", "noir", "criminal", "crime"],
            "Documentary": ["informative", "educational", "eye-opening", "real-life", "insightful", "documentary"],
            "Drama": ["emotional", "gripping", "powerful", "compelling", "intense", "drama"],
            "Family": ["heartwarming", "uplifting", "family-friendly", "enjoyable", "wholesome", "family"],
            "Fantasy": ["magical", "fantastical", "enchanting", "otherworldly", "mythical", "fantasy"],
            "Horror": ["scary", "terrifying", "spine-chilling", "haunting", "creepy", "horror"],
            "Musical": ["melodious", "harmonious", "song-filled", "entertaining", "upbeat", "musical"],
            "Mystery": ["puzzling", "enigmatic", "intriguing", "suspenseful", "mysterious", "mystery"],
            "Romance": ["romantic", "heartfelt", "passionate", "lovely", "sweet", "romance"],
            "Sci-Fi": ["futuristic", "technology-driven", "mind-bending", "sci-fi", "imaginative", "sci-fi"],
            "Thriller": ["suspenseful", "heart-pounding", "nail-biting", "tense", "exciting", "thriller"],
            "Western": ["cowboy", "wild west", "frontier", "gun-slinging", "rugged", "western"],
            "Biography": ["inspiring", "real-life", "biographical", "personal", "historic", "biography"],
            "Historical": ["period", "historical", "epic", "nostalgic", "retro", "historical"],
            "War": ["epic", "battle-filled", "wartime", "heroic", "dramatic", "war"],
            "Sports": ["athletic", "competitive", "inspiring", "sports-themed", "energetic", "sports"],
            "Supernatural": ["supernatural", "paranormal", "otherworldly", "mystical", "haunting", "supernatural"],
            "Suspense": ["suspenseful", "mysterious", "gripping", "intriguing", "nail-biting", "suspense"],
            "Noir": ["dark", "atmospheric", "noir", "moody", "brooding", "noir"],
            "Psychological": ["psychological", "mind-bending", "thought-provoking", "intriguing", "twisted", "psychological"],
            "Satire": ["satirical", "humorous", "ironic", "social-commentary", "mocking", "satire"],
            "Coming-of-Age": ["coming-of-age", "youthful", "transformative", "growing-up", "personal", "coming-of-age"],
            "Rock": ["rocking", "energetic", "upbeat", "dynamic", "catchy", "rock"],
            "Pop": ["catchy", "melodic", "upbeat", "radio-friendly", "pop", "pop"],
            "Hip Hop": ["rhythmic", "urban", "street-smart", "lyrical", "hip hop", "hip-hop"],
            "Jazz": ["sophisticated", "improvisational", "smooth", "uplifting", "jazzy", "jazz"],
            "Country": ["folksy", "nostalgic", "twangy", "heartfelt", "country", "country"],
            "Classical": ["elegant", "refined", "timeless", "orchestral", "classical", "classical"],
            "Reggae": ["laid-back", "groovy", "rhythmic", "island", "reggae", "reggae"],
            "R&B": ["soulful", "smooth", "romantic", "groovy", "r&b", "rhythm and blues"],
            "Electronic": ["electronic", "upbeat", "energetic", "synthetic", "electro", "electronic"],
            "Folk": ["acoustic", "down-to-earth", "storytelling", "rootsy", "folk", "folk"],
            "Indie": ["indie", "alternative", "quirky", "independent", "indie", "indie"],
            "Metal": ["heavy", "aggressive", "dark", "headbanging", "metal", "metal"],
            "Punk": ["rebellious", "energetic", "raw", "angsty", "punk", "punk"],
            "Blues": ["soulful", "emotional", "moody", "bluesy", "blues", "blues"],
            "Political": ["political", "socially-relevant", "controversial", "commentary", "insightful", "political"]
        }

        maxMatches = 0
        maxMatched = None
        for t in genre_adjectives:
            numMatches = 0
            for a in adjectives:
                if a in genre_adjectives[t]:
                    numMatches += 1
            if numMatches > maxMatches:
                maxMatches = numMatches
                maxMatched = t
        
        if not maxMatched:
            return "any"
        return maxMatched
        
    def findEntertainment(entertainmentType,genre):
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
        possibleChoices = []
        if entertainmentType == "movie":
            possibleChoices = []
            for m in movies:
                if movies[m].lower() == genre:
                    possibleChoices.append(m)

        if entertainmentType == "book":
            possibleChoices = []
            for b in books:
                if books[b].lower() == genre:
                    possibleChoices.append(b)

        if entertainmentType == "music":
            possibleChoices = []
            for m in music:
                if music[m].lower() == genre:
                    possibleChoices.append(m)

        if entertainmentType == "game":
            possibleChoices = []
            for g in games:
                if games[g].lower() == genre:
                    possibleChoices.append(g)

        if entertainmentType == "tv show":
            possibleChoices = []
            for t in tv_shows:
                if tv_shows[t].lower() == genre:
                    possibleChoices.append(t)

        if possibleChoices != []:
            return possibleChoices[random.randint(0,len(possibleChoices)-1)]
        else:
            return "Not Found"
    def responseSentence(chosenEntertainment,genre):
        suggestion_templates = [
            "I recommend checking out some popular GENRE options like ENTNAME.",
            "If you're into GENRE, you should definitely give ENTNAME a try.",
            "Have you considered watching ENTNAME? It's a great choice in the GENRE genre.",
            "For fans of GENRE, I suggest checking out ENTNAME. It's a fantastic option.",
            "Looking for a thrilling GENRE experience? ENTNAME is a must-watch.",
            "If you enjoy GENRE, ENTNAME is a top recommendation you shouldn't miss.",
            "ENTNAME is an excellent choice for fans of the GENRE genre.",
            "GENRE enthusiasts will love ENTNAME. Give it a go!",
            "For a great GENRE experience, I suggest watching ENTNAME.",
            "ENTNAME is a highly-rated option in the GENRE genre. Check it out!"
        ]
        chosenSentence = suggestion_templates[random.randint(0,len(suggestion_templates)-1)]

        chosenSentence = chosenSentence.replace("GENRE",genre)
        chosenSentence = chosenSentence.replace("ENTNAME",chosenEntertainment)

        return chosenSentence





    def loadKnowledge():
        print("Load Knowledge")

    def saveKnowledge():
        print("Save Knowledge")

    def part_of_speech_tagging(sentence):
        tokens = word_tokenize(sentence)
        pos_tags = pos_tag(tokens)

        nouns = []
        adjectives = []

        for word, pos in pos_tags:
            if not pos.startswith('J'):
                nouns.append(word)
                adjectives.append(word)
            elif pos.startswith('J'): 
                adjectives.append(word)
        
        return nouns, adjectives

    #Function: Tokenize User Message and Remove Stop Words
    def tokenize(message):
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

ChatBot.init()
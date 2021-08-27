import json
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import Game
from levelupapi.models import GameType


class GameTests(APITestCase):
    """
        Testing Games: creates its own database
        """
    def setUp(self):
        """
        Create a new account and create sample category
        """
        url = "/register" # register a new user
        data = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }
        # Initiate request and capture response
        response = self.client.post(url, data, format='json') # makes a post request

        # Store the auth token . LIKE NEEDING AUTHORIZATION IN THE PROVIDER FOR FETCH CALLS
        self.token = response.data["token"]

        # Assert that a user was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # SEED DATABASE WITH ONE GAME TYPE
        # This is needed because the API does not expose a /gametypes
        # endpoint for creating game types
        #this is being created here
        game_type = GameType()
        game_type.label = "Board game"
        game_type.save()


    def test_create_game(self):
        """
        Ensure we can create a new game.
        """
        # DEFINE GAME PROPERTIES
        url = "/games"
        data = {
            "gameTypeId": 1,
            "description": "This game is Awesome",
            "name": "Clue",
            "maker": "Milton Bradley",
            "numberOfPlayers": 6,
        }

        # Make sure request is authenticated. ADDS HEADERS LIKE HTTP AUTHORIZATION
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct. response.data is a dictionary
        
        self.assertEqual(response.data["name"], data ["name"])
        self.assertEqual(response.data["maker"], data ["maker"])
        self.assertEqual(response.data["description"], data ["description"])
        self.assertEqual(response.data["number_of_players"], data ["numberOfPlayers"])

    def test_get_game(self):
        """
        Ensure we can get an existing game.
        """

        # Seed the database with a game
        game = Game()
        game.game_type_id = 1
        game.description = "Crazy Fun"
        game.name = "Monopoly"
        game.maker = "Milton Bradley"
        game.number_of_players = 4
        game.gamer_id = 1

        game.save() #saves tot he database that we created and adds the ID field

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.get(f"/games/{game.id}")

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(response.data["name"], game.name)
        self.assertEqual(response.data["maker"], game.maker)
        self.assertEqual(response.data["description"], game.description)
        self.assertEqual(response.data["number_of_players"], game.number_of_players)

    def test_change_game(self):
        """
        Ensure we can change an existing game.
        """
        game = Game()
        game.game_type_id = 1
        game.description = "amazing"
        game.name = "Sorry"
        game.maker = "Milton Bradley"
        game.number_of_players = 4
        game.gamer_id = 1
        game.save()

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "gameTypeId": 1,
            "description": "cool",
            "name": "Sorry",
            "maker": "Hasbro",
            "numberOfPlayers": 4
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/games/{game.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY CHANGES
        response = self.client.get(f"/games/{game.id}")
        response.data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the properties are correct
        self.assertEqual(response.data["name"], "Sorry")
        self.assertEqual(response.data["maker"], "Hasbro")
        self.assertEqual(response.data["description"], "cool")
        self.assertEqual(response.data["number_of_players"], 4)

    def test_delete_game(self):
        """
        Ensure we can delete an existing game.
        """
        game = Game()
        game.game_type_id = 1
        game.description = "Outstanding"
        game.name = "Sorry"
        game.maker = "Milton Bradley"
        game.number_of_players = 4
        game.gamer_id = 1
        game.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY 404 response
        response = self.client.get(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

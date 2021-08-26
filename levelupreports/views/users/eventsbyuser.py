"""Module for generating games by user report"""
import sqlite3
from django.shortcuts import render
from levelupapi.models import Event
from levelupreports.views import Connection


def userevent_list(request):
    """Function to build an HTML report of games by user"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all games, with related user info.
            db_cursor.execute("""
                SELECT
                    g.id AS user_id,
                    e.id,
                    e.date,
                    e.time,                
                    e.description,
                    e.title,
                    gm.name,
                    u.id user_id,
                    u.first_name || ' ' || u.last_name AS full_name
                FROM levelupapi_event e
                JOIN levelupapi_eventgamer eg
                    ON e.id = eg.event_id
                JOIN levelupapi_gamer g ON eg.gamer_id = g.id
                JOIN auth_user u ON u.id = g.user_id
                JOIN levelupapi_game gm ON e.game_id = gm.id;
            """)

            dataset = db_cursor.fetchall()

            # Take the flat data from the database, and build the
            # following data structure for each gamer.
            #
            # {
            #     1: {
            #         "id": 1,
            #         "full_name": "Admina Straytor",
            #         "games": [
            #             {
            #                 "id": 1,
            #                 "name": "Foo",
            #                 "date": "Bar Games",
            #                 "description":"awesome",
            #                 "number_of_players": 4,
            #                 "game_type_id": 2
            #             }
            #         ]
            #     }
            # }

            events_by_user = {}

            for row in dataset:
                # Crete a Game instance and set its properties
                event = Event()
                event.title = row["name"]
                event.date = row["date"]
                event.time = row["time"]
                event.description = row["description"]                
                

                # Store the user's id
                uid = row["user_id"]

                # If the user's id is already a key in the dictionary...
                if uid in events_by_user:

                    # Add the current game to the `games` list for it
                    events_by_user[uid]['events'].append(event)

                else:
                    # Otherwise, create the key and dictionary value
                    events_by_user[uid] = {}
                    events_by_user[uid]["id"] = uid
                    events_by_user[uid]["full_name"] = row["full_name"]
                    events_by_user[uid]["events"] = [event]

        # Get only the values from the dictionary and create a list from them
        list_of_events_with_users = events_by_user.values()

        # Specify the Django template and provide data context
        template = 'users/list_with_events.html'
        context = {
            'userevent_list': list_of_events_with_users
        }

        return render(request, template, context)
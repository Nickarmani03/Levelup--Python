DROP VIEW GAMES_BY_USER
SELECT *
FROM levelupapi_gametype;
SELECT *
FROM auth_user;
SELECT *
FROM authtoken_token;
SELECT *
FROM levelupapi_gamer;
SELECT *
FROM levelupapi_games;
SELECT g.id,
    g.gametype_id,
    g.name,
    g.maker,
    g.gamer_id,
    g.number_of_players,
    g.description
FROM levelupapi_game g
SELECT g.id AS user_id,
    e.id,
    e.date,
    e.time,
    e.description,
    e.title,
    gm.name,
    u.id user_id,
    u.first_name || ' ' || u.last_name AS full_name
FROM levelupapi_event e
    JOIN levelupapi_eventgamer eg ON e.id = eg.event_id
    JOIN levelupapi_gamer g ON eg.gamer_id = g.id
    JOIN auth_user u ON u.id = g.user_id
    JOIN levelupapi_game gm ON e.game_id = gm.id;
    
CREATE VIEW GAMES_BY_USER AS
SELECT g.id,
    g.name,
    g.maker,
    g.game_type_id,
    g.number_of_players,
    g.description,
    u.id user_id,
    u.first_name || ' ' || u.last_name AS full_name
FROM levelupapi_game g
    JOIN levelupapi_gamer gr ON g.gamer_id = gr.id
    JOIN auth_user u ON gr.user_id = u.id
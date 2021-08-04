SELECT * FROM levelupapi_gametype;
SELECT * FROM auth_user;
SELECT * FROM authtoken_token;
SELECT * FROM levelupapi_gamer;
SELECT * FROM levelupapi_games;

SELECT g.id,
    g.gametype_id,
    g.title,
    g.maker,
    g.gamer_id,
    g.number_of_players,
    g.skill_level
FROM levelupapi_game g
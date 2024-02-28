# Movie_API
HW 3 for Database Structures course at TAU

18/2/24
-find out what full text query is
-Decide on what the functions will be
	-Database: https://rapidapi.com/SAdrian/api/moviesminidatabase
 	-func ideas:
  		Ideas for complex queries:
			1. Get actors frequently starring together: - movie besties, actors secretly dating,... (only actors over 18 years old and alive, if this info exsits) - attributes : movie.cast, person.id, person.name, person.dob, person.alive
			2. Get actors who have worked under 5 different directors - attributes : director_id, person.id, person.name
			3. Get movie writers who have also directed movies - attributes : movie.writer_id, movie.director_id, person.id, person.name
			4. Get recently released sequels with higher ratings than original - attributes : movie.title, movie.release_date, movie.rating, movie.series_id
			5 Get the worst movies published per year, month 2022 - timeline, per genre, or range of years.- attributes :  movie.title, movie.release_date, movie.rating, movie.genres
			6. Get the main actor in the worst movie - attributes: movie.title, movie.rating, movie.cast, person.name
			7. Suspicious movie ratings: limit by genre, find avg amount of ratings for the genre, pick top 5 movies with highest rating from movies who's # or raters is LESS than avg - attributes:movie.title, movie.rating, movie.num_ratings, genre.avg_ratings
			 
			
			Ideas for full-text queries:
			1. Search movie titles for hero or heroes
			2. Search reviews for movies referring positively to "visual effects"
			3. Search movie titles similar to 'Star Wars'
			4. Search movie titles and plots for comedy films released after 2015 with rating over 8
			5. Search reviews containing criticism of directing, acting or plot

   overall, the attributes we need : movie id, title, actors names , actors ids, ratings, director, genre, description, release year, num ratings, writer, prizes ? , reviews (and criticism), 
  	
-build database based on functions
-figure out what database update means for us- ask Bisan
	-when should it be updated? every time the python file is run?
	-google how to maintain a database using python
-figure out how to connect python to mydatabase

20/2/24
figure out how to sort and filter data we pull from rapidAPI

28.2.24

Viable queries

Actor besties by gender :
Get actors frequently starring together

SELECT 
	a1.actor_id AS actor1_id,
	a1.actor_name AS actor1_name,
	a2.actor_id AS actor2_id,
	a2.actor_name AS actor2_name,
	COUNT(*) AS movies_together_count
FROM 
	movies a1
JOIN 
	movies a2 ON a1.movie_id = a2.movie_id AND a1.actor_id < a2.actor_id
GROUP BY 
	a1.actor_id, a2.actor_id
ORDER BY 
	movies_together_count DESC;

How to optimize this search: create a table containing only movie id and actor id, index on actor ids, sorted by #

Suspicious movie ratings
limit by genre, find avg amount of ratings for the genre, pick top 5 movies with highest rating from movies who's # or raters is LESS than avg - attributes:movie.title, movie.rating, movie.num_ratings, genre.avg_ratings


**rework this so user can input genre**

WITH GenreAvgRatings AS (
	SELECT
		g.id AS Genre,
		AVG(mi.vote_count) AS AvgRatings
	FROM
		genres g
	JOIN
		Genres_movies gm ON g.Id = gm.Genres_id
	JOIN
		Movies_info mi ON gm.Movies_id = mi.Id
	WHERE
		g.name = "< genre>"
	GROUP BY
		Genre
)

SELECT
	mi.Title,
	mi.vote_average AS MovieRating,
FROM
	Movies_info mi
JOIN
	Genres_movies gm ON mi.Id = gm.Movies_id
JOIN
	GenreAvgRatings gar ON gm.Genres_id = gar.Genre //this line limits movies to chosen genre
WHERE
	mi.vote_count < gar.AvgRatings
ORDER BY
	MovieRating DESC
LIMIT 5;


Optimizations: create helper table movies_genres, index on genres

Get bottom 5 crew members by job who have the lowest avg movie ratings

WITH jobAvgRatings AS (
	SELECT
		c.Name AS crewName,
		AVG(mi.vote_average) AS AvgRating
	FROM
		Crew c
	JOIN
		Movies_info mi ON c.movie_id = mi.Id
	WHERE
		c.Job = '<job name>'
	GROUP BY
		EditorName
)

SELECT
	EditorName,
	AvgRating
FROM
	EditorAvgRatings
ORDER BY
	AvgRating ASC
LIMIT 5;

Casual movie search
Use user input to do natural language comparison against titles, taglines, and overview

SELECT 
	Title,
	release date
FROM 
	Movies_info
WHERE 
	MATCH(Tagline, overview, title) AGAINST ('<user_tagline>' IN NATURAL LANGUAGE MODE);



Weird movie recommendations 

User gives us genre or movie name. if genre we pick a random movie from that genre. We use use the text of the overview as keywords to find similar movies using match against with the overview column

Use 2 queries:

In python:
Query 1: gets keywords field from movie
Query 2: uses overview field and keyword field in match-against, returns movie titles in genres EXLUDING chosen genre/ chosen movie genre without OG movie used, sorted by ratings


Optimized by the keywords_movies table
We considered getting rid of keyword ids, mixing up the keywords and creating a full text index on keywords
But decided against it because


###########DATABASE DESIGN SO FAR##################


Info we have:

Movies
Id (PK)
Overview (FI)
release_date
Tagline (FI)
Title
vote_average
vote_count

Movie_keywords
Movie_id (FK to movies.id)
Keyword_id (FK to keywords.id)

Keywords
Id (PK)
name

Genres_movies
Genres_id (FK to genres.id)
Movies_id (FK to movies.id)

genres
Id (PK)
name

Actor_movies
Actor_id (FK to cast.id)
Movie_id (FK to movies.id)

Cast
Id (FK to person.id)

Crew
Id (FK to person.id)
Job

Person
Name
Id
Gender


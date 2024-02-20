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




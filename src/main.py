from neo4j import GraphDatabase
from flask import Flask, request, render_template

app = Flask(__name__)  

driver=GraphDatabase.driver(uri="bolt://neo4j:7687", auth=("*", "*"))
session = driver.session()


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/send", methods=["POST"])
def requesthandler():
    
    if request.form["action"] == "Show Actors":
        query = "MATCH (n: Person) RETURN n.name as name"
        records = session.run(query)
        names = []
        for record in records:
            dc = {}
            name = record["name"]
            dc.update({"Actor": name})
            names.append(dc)
        return render_template("actors.html", list=names)
     
    elif request.form["action"] == "Show Movies":
        query = "MATCH (n: Movie) RETURN n.title as title"
        records = session.run(query)
        titles = []
        for record in records:
            dc = {}
            title = record["title"]
            dc.update({"Movie": title})
            titles.append(dc)
        return render_template("movies.html", list=titles)

    elif request.form["action"] == "Find Movies":
        actor = request.form["movie_actor"]
        query = """
        MATCH(actor: Person{name: $actor})-[:ACTED_IN]->(movies)
        RETURN actor,movies
        """
        parameter = {"actor": actor}
        records= session.run(query, parameter)
        movies_title = []
        for record in records:
            actor_name = record["actor"]["name"]
            movie = record["movies"]["title"]
            movies_title.append(movie)
        if (len(movies_title) > 0):
            return render_template("movies_actor.html", name=actor_name, movies = movies_title)
        else:
            return ("no actor or invalid input")
    
    elif request.form["action"] == "Find Actors":
        movie = request.form["actor_movie"]
        query = """
        MATCH(movie: Movie{title: $movie})<-[:ACTED_IN]-(actors)
        RETURN movie,actors
        """
        parameter = {"movie": movie}
        records= session.run(query, parameter)
        actors_name = []
        for record in records:
            movie_title = record["movie"]["title"]
            actor = record["actors"]["name"]
            actors_name.append(actor)
        if (len(actors_name) > 0):
            return render_template("actors_movie.html", title=movie_title, actors = actors_name)
        else:
            return ("no movie or invalid input")
       

if __name__ == '__main__':
    app.run(host="0.0.0.0")






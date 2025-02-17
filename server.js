import express from "express"
import path from "path"
import { readFileSync } from "fs";
import { GraphQLClient, gql } from 'graphql-request'


// Functions
async function get_battle (id) {
  const query = gql`{
	battle(id: "`+id+`") {
		events
		players {
			id
			name
		}
		finishedAt
    winner {
      name
    }
	}
}`;
  const client = new GraphQLClient('https://battletabs.fly.dev/graphql');
  const data = await client.request(query);
  return data;
};


// Express
const app = express();
const port = 3000; 

app.set('view engine', 'ejs');

app.use(express.static("static"));

app.get('/', (req, res) => {
  res.render('index');
});

app.get("/upload", (req, res) => {
  res.render("upload");
});

app.get("/player", (req, res) => {
  const q = req.query
  const playerid = q.id
  if (playerid===undefined) {
    res.render("notfound");
  } else {
    var players = JSON.parse(readFileSync("db/player.json", "utf8"))
    console.log(players)

    res.render("player", { playerid });
  }
  res.render("player");
});

app.get("/viewer", async function (req, res) {
  const q = req.query
  if (q.id===undefined) {
    res.render("notfound");
  } else {
    var data = await get_battle(q.id)
    console.log(data)
    res.render("viewer", { data });
  }
});

app.listen(port, () => {
  console.log(`Server is listening at http://localhost:${port}`);
});
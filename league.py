from modules import battletabs

auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI5YmM3YzdlNy0xY2ViLTQ4YjAtYTAwMC0xOTI4Y2I2MTU0ZTgiLCJyb2xlcyI6WyJ1c2VyIl0sImlhdCI6MTczMDY5Mjk4OCwiZXhwIjoxNzMxMjk3Nzg4fQ.t4FExu5pd44SaTQxuXdvSVUwbA83wkm-93lCe_0UjBI"

client = battletabs.BattleTabsClient(auth_token)

print(client.query("{myLeagueProgress {trophies\ndiamonds}}"))

open("league.json", "w").write(str(client.query("{leaguePlayers\n {id\ntrophies}}")))

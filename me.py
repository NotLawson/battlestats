from modules import battletabs
import json

auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI5YmM3YzdlNy0xY2ViLTQ4YjAtYTAwMC0xOTI4Y2I2MTU0ZTgiLCJyb2xlcyI6WyJ1c2VyIl0sImlhdCI6MTczMDY5Mjk4OCwiZXhwIjoxNzMxMjk3Nzg4fQ.t4FExu5pd44SaTQxuXdvSVUwbA83wkm-93lCe_0UjBI"

client = battletabs.BattleTabsClient(auth_token)

open("out.json", "w").write(json.dumps(client.query("{me {name\nemail\nid\nsettings\nprimaryFleet}}")))
#open("out.json", "w").write(json.dumps(client.query("{me {stats {wins\nlosses}\nenhancedStats}}")))
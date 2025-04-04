import os, json

o = json.load(open("battle.json"))
events = o["data"]["battle"]["events"]

types = []
for event in events:
    if event["kind"] not in types:
        types.append(event["kind"])

print(events.index({
    "id": "-6aReNyeji",
    "kind": "turn-timed-out",
    "createdAt": 1742675715920,
    "timeoutByUserId": "b0c413f9-856b-4814-b460-7a0accbf23cc"
}))
input(types)

for event in events:
    print(json.dumps(event, indent=4))
    c = input("")
    if c == "c":
        os.system('cls')
        

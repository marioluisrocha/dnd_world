# API Usage Examples

This document provides examples of how to use the D&D Campaign Manager API.

Base URL: `http://localhost:8000/api/v1`

## Authentication

### Register a New User

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "dm@example.com",
    "username": "dungeon_master",
    "password": "SecurePassword123"
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=dungeon_master&password=SecurePassword123"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Get Current User

```bash
curl -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Campaigns

### Create a Campaign

```bash
curl -X POST "http://localhost:8000/api/v1/campaigns" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Lost Mine of Phandelver",
    "description": "A starter adventure for new players",
    "setting": "Forgotten Realms",
    "is_active": true
  }'
```

### List All Campaigns

```bash
curl -X GET "http://localhost:8000/api/v1/campaigns" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Get Campaign Details

```bash
curl -X GET "http://localhost:8000/api/v1/campaigns/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Update a Campaign

```bash
curl -X PUT "http://localhost:8000/api/v1/campaigns/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Updated description"
  }'
```

### Add Member to Campaign

```bash
curl -X POST "http://localhost:8000/api/v1/campaigns/1/members" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 2,
    "role": "player"
  }'
```

## Characters

### Create a Character

```bash
curl -X POST "http://localhost:8000/api/v1/characters" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Thorin Ironshield",
    "campaign_id": 1,
    "race": "Dwarf",
    "character_class": "Fighter",
    "level": 3,
    "background": "Soldier",
    "alignment": "Lawful Good",
    "stats": {
      "str": 16,
      "dex": 12,
      "con": 15,
      "int": 10,
      "wis": 13,
      "cha": 8
    },
    "backstory": "A veteran soldier seeking glory...",
    "is_npc": false
  }'
```

### List Characters in a Campaign

```bash
curl -X GET "http://localhost:8000/api/v1/characters/campaign/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Import from D&D Beyond

```bash
curl -X POST "http://localhost:8000/api/v1/dndbeyond/import" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_id": 1,
    "character_url": "https://www.dndbeyond.com/characters/12345678",
    "cobalt_token": "YOUR_COBALT_TOKEN"
  }'
```

## Places

### Create a Place

```bash
curl -X POST "http://localhost:8000/api/v1/places" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Phandalin",
    "campaign_id": 1,
    "place_type": "town",
    "description": "A small frontier town",
    "population": 1000,
    "notable_npcs": "Sildar Hallwinter, Toblen Stonehill",
    "secrets": "Hidden cultists operate in the basement..."
  }'
```

### Create Nested Place

```bash
curl -X POST "http://localhost:8000/api/v1/places" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Stonehill Inn",
    "campaign_id": 1,
    "place_type": "building",
    "parent_place_id": 1,
    "description": "The local inn and tavern"
  }'
```

## Items

### Create an Item

```bash
curl -X POST "http://localhost:8000/api/v1/items" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Flametongue Longsword",
    "campaign_id": 1,
    "item_type": "weapon",
    "rarity": "rare",
    "description": "You can use a bonus action to make flames erupt from the blade",
    "damage": "1d8 slashing + 2d6 fire",
    "value": 5000,
    "weight": 3,
    "requires_attunement": true,
    "is_magical": true
  }'
```

### List Campaign Items

```bash
curl -X GET "http://localhost:8000/api/v1/items/campaign/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Quests

### Create a Quest

```bash
curl -X POST "http://localhost:8000/api/v1/quests" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Find Gundren Rockseeker",
    "campaign_id": 1,
    "description": "Rescue Gundren from the goblins",
    "objectives": "1. Track the goblins\n2. Infiltrate hideout\n3. Rescue Gundren",
    "rewards": "100 gold pieces",
    "quest_giver": "Sildar Hallwinter",
    "location": "Cragmaw Hideout",
    "status": "in_progress"
  }'
```

### Update Quest Status

```bash
curl -X PUT "http://localhost:8000/api/v1/quests/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed"
  }'
```

## Sessions

### Create a Session

```bash
curl -X POST "http://localhost:8000/api/v1/sessions" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_id": 1,
    "session_number": 1,
    "title": "The Adventure Begins",
    "summary": "The party met in Neverwinter and traveled to Phandalin...",
    "notes": "Players enjoyed the goblin ambush encounter",
    "session_date": "2024-01-15",
    "duration_minutes": 240
  }'
```

### List Campaign Sessions

```bash
curl -X GET "http://localhost:8000/api/v1/sessions/campaign/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Notes

### Create a Note

```bash
curl -X POST "http://localhost:8000/api/v1/notes" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_id": 1,
    "title": "Black Spider Plot",
    "content": "The Black Spider is actually Nezznar, a drow seeking the Forge of Spells...",
    "category": "Plot",
    "tags": "villain,drow,main-plot",
    "is_dm_only": true
  }'
```

### List Campaign Notes

```bash
curl -X GET "http://localhost:8000/api/v1/notes/campaign/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Python Examples

### Using requests library

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Login
response = requests.post(
    f"{BASE_URL}/auth/login",
    data={"username": "dungeon_master", "password": "SecurePassword123"}
)
token = response.json()["access_token"]

# Headers for authenticated requests
headers = {"Authorization": f"Bearer {token}"}

# Create a campaign
campaign = requests.post(
    f"{BASE_URL}/campaigns",
    json={
        "name": "Curse of Strahd",
        "description": "Gothic horror adventure",
        "setting": "Ravenloft"
    },
    headers=headers
).json()

print(f"Created campaign: {campaign['name']}")

# List all campaigns
campaigns = requests.get(f"{BASE_URL}/campaigns", headers=headers).json()
for camp in campaigns:
    print(f"- {camp['name']}")
```

## JavaScript/TypeScript Examples

### Using axios

```typescript
import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

// Login
const { data: { access_token } } = await axios.post(`${API_URL}/auth/login`,
  new URLSearchParams({
    username: 'dungeon_master',
    password: 'SecurePassword123'
  })
);

// Create axios instance with auth
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Authorization': `Bearer ${access_token}`
  }
});

// Create a character
const character = await api.post('/characters', {
  name: 'Elara Moonwhisper',
  campaign_id: 1,
  race: 'Elf',
  character_class: 'Wizard',
  level: 5,
  stats: { str: 8, dex: 14, con: 12, int: 18, wis: 13, cha: 10 }
});

console.log('Created character:', character.data);
```

## Error Handling

The API returns standard HTTP status codes:

- `200 OK` - Request succeeded
- `201 Created` - Resource created successfully
- `204 No Content` - Resource deleted successfully
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Missing or invalid authentication
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

Error response format:
```json
{
  "detail": "Error message here"
}
```

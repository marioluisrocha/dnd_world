export interface User {
  id: number
  email: string
  username: string
  is_active: boolean
  created_at: string
}

export interface Campaign {
  id: number
  name: string
  description?: string
  setting?: string
  is_active: boolean
  owner_id: number
  created_at: string
  updated_at?: string
}

export interface Character {
  id: number
  name: string
  campaign_id: number
  creator_id: number
  race?: string
  character_class?: string
  level: number
  background?: string
  alignment?: string
  stats?: Record<string, number>
  backstory?: string
  personality_traits?: string
  ideals?: string
  bonds?: string
  flaws?: string
  appearance?: string
  is_npc: boolean
  is_active: boolean
  dndbeyond_url?: string
  created_at: string
}

export interface Place {
  id: number
  name: string
  campaign_id: number
  place_type: string
  description?: string
  history?: string
  notable_npcs?: string
  secrets?: string
  population?: number
  climate?: string
  terrain?: string
  map_image_url?: string
  created_at: string
}

export interface Item {
  id: number
  name: string
  campaign_id: number
  item_type: string
  rarity: string
  description?: string
  properties?: string
  weight?: number
  value?: number
  damage?: string
  requires_attunement: boolean
  is_magical: boolean
  is_cursed: boolean
  created_at: string
}

export interface Quest {
  id: number
  name: string
  campaign_id: number
  description?: string
  objectives?: string
  rewards?: string
  quest_giver?: string
  location?: string
  status: string
  created_at: string
}

export interface LoginCredentials {
  username: string
  password: string
}

export interface RegisterData {
  email: string
  username: string
  password: string
}

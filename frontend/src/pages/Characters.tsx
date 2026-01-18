import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '../services/api'

interface Campaign {
  id: number
  name: string
}

interface Character {
  id: number
  name: string
  race: string
  character_class: string
  level: number
  campaign_id: number
  is_npc: boolean
  dndbeyond_url?: string
}

export default function Characters() {
  const [selectedCampaignId, setSelectedCampaignId] = useState<number | null>(null)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [showImportModal, setShowImportModal] = useState(false)
  const queryClient = useQueryClient()

  // Fetch campaigns
  const { data: campaigns } = useQuery<Campaign[]>({
    queryKey: ['campaigns'],
    queryFn: async () => {
      const response = await api.get('/campaigns')
      return response.data
    },
  })

  // Fetch characters for selected campaign
  const { data: characters, isLoading: loadingCharacters } = useQuery<Character[]>({
    queryKey: ['characters', selectedCampaignId],
    queryFn: async () => {
      const response = await api.get(`/characters/campaign/${selectedCampaignId}`)
      return response.data
    },
    enabled: !!selectedCampaignId,
  })

  // Import from D&D Beyond
  const importFromDnDBeyond = useMutation({
    mutationFn: async (data: { campaign_id: number; character_url: string; cobalt_token?: string }) => {
      const response = await api.post('/dndbeyond/import', data)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['characters', selectedCampaignId] })
      setShowImportModal(false)
    },
  })

  // Create character manually
  const createCharacter = useMutation({
    mutationFn: async (data: any) => {
      const response = await api.post('/characters', data)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['characters', selectedCampaignId] })
      setShowCreateModal(false)
    },
  })

  // Delete character
  const deleteCharacter = useMutation({
    mutationFn: async (characterId: number) => {
      await api.delete(`/characters/${characterId}`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['characters', selectedCampaignId] })
    },
  })

  const handleImport = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    importFromDnDBeyond.mutate({
      campaign_id: selectedCampaignId!,
      character_url: formData.get('character_url') as string,
      cobalt_token: formData.get('cobalt_token') as string || undefined,
    })
  }

  const handleCreate = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    createCharacter.mutate({
      campaign_id: selectedCampaignId,
      name: formData.get('name') as string,
      race: formData.get('race') as string,
      character_class: formData.get('character_class') as string,
      level: parseInt(formData.get('level') as string) || 1,
      background: formData.get('background') as string,
      alignment: formData.get('alignment') as string,
    })
  }

  return (
    <div className="px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Characters</h1>
      </div>

      {/* Campaign Selector */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Select Campaign
        </label>
        <select
          value={selectedCampaignId || ''}
          onChange={(e) => setSelectedCampaignId(e.target.value ? Number(e.target.value) : null)}
          className="input max-w-md"
        >
          <option value="">Choose a campaign...</option>
          {campaigns?.map((campaign) => (
            <option key={campaign.id} value={campaign.id}>
              {campaign.name}
            </option>
          ))}
        </select>
      </div>

      {selectedCampaignId && (
        <>
          <div className="flex gap-3 mb-6">
            <button
              onClick={() => setShowCreateModal(true)}
              className="btn btn-primary"
            >
              Create Character
            </button>
            <button
              onClick={() => setShowImportModal(true)}
              className="btn"
            >
              Import from D&D Beyond
            </button>
          </div>

          {loadingCharacters ? (
            <div className="card">
              <p className="text-gray-600">Loading characters...</p>
            </div>
          ) : characters && characters.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {characters.map((character) => (
                <div key={character.id} className="card hover:shadow-lg transition-shadow">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="text-xl font-semibold text-gray-900">
                      {character.name}
                    </h3>
                    <div className="flex items-center gap-2">
                      {character.is_npc && (
                        <span className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs">
                          NPC
                        </span>
                      )}
                      <button
                        onClick={() => {
                          if (confirm(`Delete ${character.name}?`)) {
                            deleteCharacter.mutate(character.id)
                          }
                        }}
                        className="text-red-600 hover:text-red-800 text-sm"
                        title="Delete character"
                      >
                        ×
                      </button>
                    </div>
                  </div>
                  <p className="text-gray-600 text-sm mb-2">
                    {character.race} {character.character_class}
                  </p>
                  <p className="text-gray-500 text-sm">
                    Level {character.level}
                  </p>
                  {character.dndbeyond_url && (
                    <a
                      href={character.dndbeyond_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm text-blue-600 hover:text-blue-800 mt-2 inline-block"
                    >
                      View on D&D Beyond
                    </a>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div className="card">
              <p className="text-gray-600">
                No characters yet. Create one or import from D&D Beyond!
              </p>
            </div>
          )}
        </>
      )}

      {!selectedCampaignId && campaigns && campaigns.length > 0 && (
        <div className="card">
          <p className="text-gray-600">
            Select a campaign to view and manage characters.
          </p>
        </div>
      )}

      {!selectedCampaignId && (!campaigns || campaigns.length === 0) && (
        <div className="card">
          <p className="text-gray-600">
            No campaigns found. Create a campaign first to add characters.
          </p>
        </div>
      )}

      {/* Import from D&D Beyond Modal */}
      {showImportModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <h2 className="text-2xl font-bold mb-4">Import from D&D Beyond</h2>
            <form onSubmit={handleImport}>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Character URL
                </label>
                <input
                  type="url"
                  name="character_url"
                  required
                  className="input"
                  placeholder="https://www.dndbeyond.com/characters/12345"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Paste your D&D Beyond character sheet URL
                </p>
              </div>
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Cobalt Token (Optional)
                </label>
                <input
                  type="text"
                  name="cobalt_token"
                  className="input"
                  placeholder="Your CobaltSession cookie value"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Required for private character sheets. Find this in your browser cookies when logged into D&D Beyond.
                </p>
              </div>
              {importFromDnDBeyond.isError && (
                <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded text-sm text-red-700">
                  <p className="font-semibold mb-1">Failed to import character</p>
                  <p>
                    {importFromDnDBeyond.error?.response?.data?.detail ||
                     "D&D Beyond requires a Cobalt session token to import characters. Please provide your token above."}
                  </p>
                </div>
              )}
              <div className="flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setShowImportModal(false)}
                  className="btn"
                  disabled={importFromDnDBeyond.isPending}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={importFromDnDBeyond.isPending}
                >
                  {importFromDnDBeyond.isPending ? 'Importing...' : 'Import'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Create Character Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full max-h-[90vh] overflow-y-auto">
            <h2 className="text-2xl font-bold mb-4">Create Character</h2>
            <form onSubmit={handleCreate}>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Name
                </label>
                <input
                  type="text"
                  name="name"
                  required
                  className="input"
                  placeholder="Character name"
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Race
                </label>
                <input
                  type="text"
                  name="race"
                  className="input"
                  placeholder="e.g., Human, Elf, Dwarf"
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Class
                </label>
                <input
                  type="text"
                  name="character_class"
                  className="input"
                  placeholder="e.g., Fighter, Wizard, Rogue"
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Level
                </label>
                <input
                  type="number"
                  name="level"
                  min="1"
                  max="20"
                  defaultValue="1"
                  className="input"
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Background
                </label>
                <input
                  type="text"
                  name="background"
                  className="input"
                  placeholder="e.g., Soldier, Noble, Outlander"
                />
              </div>
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Alignment
                </label>
                <select name="alignment" className="input">
                  <option value="">Select alignment</option>
                  <option value="Lawful Good">Lawful Good</option>
                  <option value="Neutral Good">Neutral Good</option>
                  <option value="Chaotic Good">Chaotic Good</option>
                  <option value="Lawful Neutral">Lawful Neutral</option>
                  <option value="True Neutral">True Neutral</option>
                  <option value="Chaotic Neutral">Chaotic Neutral</option>
                  <option value="Lawful Evil">Lawful Evil</option>
                  <option value="Neutral Evil">Neutral Evil</option>
                  <option value="Chaotic Evil">Chaotic Evil</option>
                </select>
              </div>
              <div className="flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="btn"
                >
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  Create
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

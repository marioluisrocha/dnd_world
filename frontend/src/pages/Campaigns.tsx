import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '../services/api'
import { useNavigate } from 'react-router-dom'

interface Campaign {
  id: number
  name: string
  description: string
  setting: string
  is_active: boolean
  owner_id: number
  created_at: string
}

interface CampaignMember {
  id: number
  user_id: number
  role: 'dm' | 'player' | 'viewer'
  joined_at: string
  user: {
    id: number
    username: string
    email: string
  }
}

interface CampaignDetail extends Campaign {
  members: CampaignMember[]
  owner: {
    id: number
    username: string
    email: string
  }
}

export default function Campaigns() {
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [selectedCampaign, setSelectedCampaign] = useState<number | null>(null)
  const queryClient = useQueryClient()
  const navigate = useNavigate()

  // Fetch campaigns
  const { data: campaigns, isLoading } = useQuery<Campaign[]>({
    queryKey: ['campaigns'],
    queryFn: async () => {
      const response = await api.get('/campaigns')
      return response.data
    },
  })

  // Fetch campaign details
  const { data: campaignDetail } = useQuery<CampaignDetail>({
    queryKey: ['campaign', selectedCampaign],
    queryFn: async () => {
      const response = await api.get(`/campaigns/${selectedCampaign}`)
      return response.data
    },
    enabled: !!selectedCampaign,
  })

  // Create campaign mutation
  const createCampaign = useMutation({
    mutationFn: async (data: { name: string; description: string; setting: string }) => {
      const response = await api.post('/campaigns', data)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['campaigns'] })
      setShowCreateModal(false)
    },
  })

  // Delete campaign mutation
  const deleteCampaign = useMutation({
    mutationFn: async (id: number) => {
      await api.delete(`/campaigns/${id}`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['campaigns'] })
      setSelectedCampaign(null)
    },
  })

  const handleCreateCampaign = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    createCampaign.mutate({
      name: formData.get('name') as string,
      description: formData.get('description') as string,
      setting: formData.get('setting') as string,
    })
  }

  if (isLoading) {
    return (
      <div className="px-4 py-8">
        <p>Loading campaigns...</p>
      </div>
    )
  }

  return (
    <div className="px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Campaigns</h1>
        <button
          onClick={() => setShowCreateModal(true)}
          className="btn btn-primary"
        >
          Create Campaign
        </button>
      </div>

      {campaigns && campaigns.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {campaigns.map((campaign) => (
            <div
              key={campaign.id}
              className="card hover:shadow-lg transition-shadow cursor-pointer"
              onClick={() => setSelectedCampaign(campaign.id)}
            >
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                {campaign.name}
              </h3>
              <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                {campaign.description || 'No description'}
              </p>
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-500">{campaign.setting || 'No setting'}</span>
                <span className={`px-2 py-1 rounded ${campaign.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                  {campaign.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="card">
          <p className="text-gray-600">
            Your campaigns will appear here. Create your first campaign to get started!
          </p>
        </div>
      )}

      {/* Create Campaign Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <h2 className="text-2xl font-bold mb-4">Create Campaign</h2>
            <form onSubmit={handleCreateCampaign}>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Campaign Name
                </label>
                <input
                  type="text"
                  name="name"
                  required
                  className="input"
                  placeholder="The Lost Mines of Phandelver"
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Description
                </label>
                <textarea
                  name="description"
                  rows={3}
                  className="input"
                  placeholder="A tale of adventure in the Sword Coast..."
                />
              </div>
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Setting
                </label>
                <input
                  type="text"
                  name="setting"
                  className="input"
                  placeholder="Forgotten Realms, Homebrew, etc."
                />
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

      {/* Campaign Detail Modal */}
      {selectedCampaign && campaignDetail && (
        <CampaignDetailModal
          campaign={campaignDetail}
          onClose={() => setSelectedCampaign(null)}
          onDelete={() => deleteCampaign.mutate(selectedCampaign)}
        />
      )}
    </div>
  )
}

interface SearchUser {
  id: number
  username: string
  email: string
}

// Campaign Detail Modal Component
function CampaignDetailModal({
  campaign,
  onClose,
  onDelete,
}: {
  campaign: CampaignDetail
  onClose: () => void
  onDelete: () => void
}) {
  const [showAddMember, setShowAddMember] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState<SearchUser[]>([])
  const [selectedUser, setSelectedUser] = useState<SearchUser | null>(null)
  const [memberRole, setMemberRole] = useState<'dm' | 'player' | 'viewer'>('player')
  const [isSearching, setIsSearching] = useState(false)
  const queryClient = useQueryClient()

  // Search users
  const searchUsers = async (query: string) => {
    if (query.length < 2) {
      setSearchResults([])
      return
    }

    setIsSearching(true)
    try {
      const response = await api.get('/users/search', { params: { q: query } })
      setSearchResults(response.data)
    } catch (error) {
      console.error('Search error:', error)
      setSearchResults([])
    } finally {
      setIsSearching(false)
    }
  }

  // Debounce search
  const handleSearchChange = (value: string) => {
    setSearchQuery(value)
    setSelectedUser(null)

    // Simple debounce
    const timeoutId = setTimeout(() => {
      searchUsers(value)
    }, 300)

    return () => clearTimeout(timeoutId)
  }

  // Add member mutation
  const addMember = useMutation({
    mutationFn: async (data: { user_id: number; role: string }) => {
      await api.post(`/campaigns/${campaign.id}/members`, data)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['campaign', campaign.id] })
      setShowAddMember(false)
      setSearchQuery('')
      setSearchResults([])
      setSelectedUser(null)
    },
  })

  // Remove member mutation
  const removeMember = useMutation({
    mutationFn: async (userId: number) => {
      await api.delete(`/campaigns/${campaign.id}/members/${userId}`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['campaign', campaign.id] })
    },
  })

  const handleAddMember = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!selectedUser) {
      alert('Please select a user from the search results')
      return
    }

    addMember.mutate({
      user_id: selectedUser.id,
      role: memberRole,
    })
  }

  console.log('CampaignDetailModal rendering:', campaign)

  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
      onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}
    >
      <div className="bg-white rounded-lg p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-start mb-6">
          <div>
            <h2 className="text-2xl font-bold">{campaign.name}</h2>
            <p className="text-gray-600 text-sm">
              by {campaign.owner.username}
            </p>
          </div>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div className="mb-6">
          <h3 className="font-semibold mb-2">Description</h3>
          <p className="text-gray-700">{campaign.description || 'No description'}</p>
        </div>

        <div className="mb-6">
          <h3 className="font-semibold mb-2">Setting</h3>
          <p className="text-gray-700">{campaign.setting || 'Not specified'}</p>
        </div>

        <div className="mb-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="font-semibold">Members ({campaign.members?.length || 0})</h3>
            <button
              onClick={() => setShowAddMember(!showAddMember)}
              className="text-sm btn btn-primary"
            >
              Add Member
            </button>
          </div>

          {showAddMember && (
            <form onSubmit={handleAddMember} className="mb-4 p-4 bg-gray-50 rounded">
              <div className="mb-3">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Search User
                </label>
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => handleSearchChange(e.target.value)}
                  className="input text-sm"
                  placeholder="Search by email or username..."
                  autoComplete="off"
                />

                {/* Search Results Dropdown */}
                {searchQuery.length >= 2 && (
                  <div className="mt-2 border border-gray-200 rounded bg-white max-h-48 overflow-y-auto">
                    {isSearching ? (
                      <div className="p-3 text-sm text-gray-500">Searching...</div>
                    ) : searchResults.length > 0 ? (
                      searchResults.map((user) => (
                        <div
                          key={user.id}
                          onClick={() => {
                            setSelectedUser(user)
                            setSearchQuery(`${user.username} (${user.email})`)
                            setSearchResults([])
                          }}
                          className="p-3 hover:bg-gray-100 cursor-pointer border-b last:border-b-0"
                        >
                          <div className="font-medium text-sm">{user.username}</div>
                          <div className="text-xs text-gray-600">{user.email}</div>
                        </div>
                      ))
                    ) : (
                      <div className="p-3 text-sm text-gray-500">No users found</div>
                    )}
                  </div>
                )}

                {selectedUser && (
                  <div className="mt-2 p-2 bg-blue-50 border border-blue-200 rounded text-sm">
                    Selected: <span className="font-medium">{selectedUser.username}</span>
                  </div>
                )}
              </div>
              <div className="mb-3">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Role
                </label>
                <select
                  value={memberRole}
                  onChange={(e) => setMemberRole(e.target.value as any)}
                  className="input text-sm"
                >
                  <option value="player">Player</option>
                  <option value="dm">Dungeon Master</option>
                  <option value="viewer">Viewer</option>
                </select>
              </div>
              <div className="flex gap-2">
                <button
                  type="submit"
                  className="btn btn-primary text-sm"
                  disabled={!selectedUser}
                >
                  Add
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowAddMember(false)
                    setSearchQuery('')
                    setSearchResults([])
                    setSelectedUser(null)
                  }}
                  className="btn text-sm"
                >
                  Cancel
                </button>
              </div>
            </form>
          )}

          <div className="space-y-2">
            {campaign.members && campaign.members.length > 0 ? (
              campaign.members.map((member) => (
                <div
                  key={member.id}
                  className="flex items-center justify-between p-3 bg-gray-50 rounded"
                >
                  <div>
                    <p className="font-medium">{member.user.username}</p>
                    <p className="text-sm text-gray-600">{member.user.email}</p>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className={`px-2 py-1 rounded text-xs font-medium ${
                      member.role === 'dm' ? 'bg-purple-100 text-purple-800' :
                      member.role === 'player' ? 'bg-blue-100 text-blue-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {member.role.toUpperCase()}
                    </span>
                    <button
                      onClick={() => removeMember.mutate(member.user_id)}
                      className="text-red-600 hover:text-red-800 text-sm"
                    >
                      Remove
                    </button>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-gray-500 text-sm">No members yet</p>
            )}
          </div>
        </div>

        <div className="flex justify-between pt-4 border-t">
          <button
            onClick={onDelete}
            className="btn text-red-600 hover:bg-red-50"
          >
            Delete Campaign
          </button>
          <button onClick={onClose} className="btn">
            Close
          </button>
        </div>
      </div>
    </div>
  )
}

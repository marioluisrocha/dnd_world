# Next Steps - Implementation Roadmap

This guide will help you complete the D&D Campaign Manager platform step by step.

## Current Status: Foundation Complete ✅

- Backend API: 100% functional
- Database schema: Complete
- Authentication: Working
- Frontend structure: Ready
- Docker setup: Configured

## Phase 1: Get It Running (30 minutes)

### Option A: Using Docker (Recommended)

```bash
# 1. Ensure Docker is running
docker --version
docker-compose --version

# 2. Start all services
docker-compose up --build

# 3. In another terminal, seed the database
docker-compose exec backend python init_db.py --seed

# 4. Open browser
# Frontend: http://localhost:5173
# API Docs: http://localhost:8000/docs
# Test login: dungeon_master / password123
```

### Option B: Manual Setup

```bash
# 1. Start PostgreSQL (if not running)
# Make sure PostgreSQL is installed and running

# 2. Create database
createdb dnd_world

# 3. Setup backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 4. Update .env with your PostgreSQL credentials
# DATABASE_URL=postgresql://your_user:your_password@localhost:5432/dnd_world

# 5. Initialize database
python init_db.py --seed

# 6. Start backend
uvicorn app.main:app --reload

# 7. In another terminal, setup frontend
cd frontend
npm install
npm run dev

# 8. Access
# Frontend: http://localhost:5173
# Backend: http://localhost:8000
```

## Phase 2: Test the Backend API (15 minutes)

Test that everything works using the Swagger UI at http://localhost:8000/docs

1. **Register a user** (POST /api/v1/auth/register)
2. **Login** (POST /api/v1/auth/login) - Copy the access token
3. **Click "Authorize"** button in Swagger UI - Paste token as "Bearer YOUR_TOKEN"
4. **Test endpoints**:
   - GET /api/v1/users/me
   - POST /api/v1/campaigns (create a campaign)
   - GET /api/v1/campaigns (list campaigns)
   - POST /api/v1/characters (create a character)

## Phase 3: Frontend Development Priority

### Week 1: Campaign Management (High Priority)

**Files to create/modify:**

#### 1. Campaign List with Data Fetching
**File**: `frontend/src/pages/Campaigns.tsx`

Add React Query to fetch and display campaigns:
- Fetch campaigns from API
- Display in a grid/list
- Add "Create Campaign" button
- Show loading/error states

#### 2. Campaign Creation Modal/Form
**File**: `frontend/src/components/CampaignForm.tsx`

Create form component with:
- Name, description, setting fields
- Submit handler
- Validation
- Success/error feedback

#### 3. Campaign Detail Page
**File**: `frontend/src/pages/CampaignDetail.tsx`

Build out the detail view:
- Tabs for Characters, Places, Items, Quests, Sessions, Notes
- Campaign info display
- Edit/delete buttons
- Member management

### Week 2: Character Management

#### 4. Character List Page
**File**: `frontend/src/pages/Characters.tsx`

- Fetch characters for selected campaign
- Character cards with basic info
- Filter NPCs vs PCs
- Create character button

#### 5. Character Sheet Component
**File**: `frontend/src/components/CharacterSheet.tsx`

Build a D&D character sheet view:
- Stats display
- Class, race, level
- Backstory, traits
- Inventory tab

#### 6. Character Form
**File**: `frontend/src/components/CharacterForm.tsx`

Multi-step form:
- Basic info (name, race, class, level)
- Stats input
- Backstory fields
- D&D Beyond import option

### Week 3: World Building & Items

#### 7. Places Management
**File**: `frontend/src/pages/Places.tsx`

- Hierarchical place view
- Create/edit places
- Place detail view
- Map integration placeholder

#### 8. Items Management
**File**: `frontend/src/pages/Items.tsx`

- Item list with filters (type, rarity)
- Create/edit item form
- Item detail view

#### 9. Quest Tracker
**File**: `frontend/src/components/QuestTracker.tsx`

- Quest kanban board (Not Started, In Progress, Completed)
- Drag-and-drop to update status
- Quick add quest

### Week 4: Polish & Features

#### 10. Session Log
- Session creation/editing
- Timeline view
- Session notes

#### 11. Campaign Notes
- Note list with categories
- DM-only toggle
- Rich text editor

#### 12. Search & Filter
- Global search component
- Filter by campaign
- Quick navigation

## Recommended Implementation Order

### Step 1: Campaign CRUD (Start Here) ⭐

```typescript
// frontend/src/hooks/useCampaigns.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api from '../services/api'
import { Campaign } from '../types'

export const useCampaigns = () => {
  return useQuery({
    queryKey: ['campaigns'],
    queryFn: async () => {
      const { data } = await api.get<Campaign[]>('/campaigns')
      return data
    }
  })
}

export const useCreateCampaign = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (newCampaign: Partial<Campaign>) => {
      const { data } = await api.post('/campaigns', newCampaign)
      return data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['campaigns'] })
    }
  })
}
```

### Step 2: Update Campaigns Page

```typescript
// frontend/src/pages/Campaigns.tsx
import { useState } from 'react'
import { useCampaigns, useCreateCampaign } from '../hooks/useCampaigns'
import CampaignCard from '../components/CampaignCard'
import CreateCampaignModal from '../components/CreateCampaignModal'

export default function Campaigns() {
  const [showModal, setShowModal] = useState(false)
  const { data: campaigns, isLoading, error } = useCampaigns()
  const createCampaign = useCreateCampaign()

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error loading campaigns</div>

  return (
    <div className="px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Campaigns</h1>
        <button
          onClick={() => setShowModal(true)}
          className="btn btn-primary"
        >
          Create Campaign
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {campaigns?.map(campaign => (
          <CampaignCard key={campaign.id} campaign={campaign} />
        ))}
      </div>

      {showModal && (
        <CreateCampaignModal
          onClose={() => setShowModal(false)}
          onCreate={(data) => {
            createCampaign.mutate(data)
            setShowModal(false)
          }}
        />
      )}
    </div>
  )
}
```

### Step 3: Create Reusable Components

Components you'll need:
- `CampaignCard.tsx` - Display campaign summary
- `CreateCampaignModal.tsx` - Modal with form
- `CharacterCard.tsx` - Display character summary
- `Modal.tsx` - Reusable modal wrapper
- `LoadingSpinner.tsx` - Loading indicator
- `ErrorMessage.tsx` - Error display

## Tools & Libraries to Add

```bash
cd frontend

# UI Components (optional but recommended)
npm install @headlessui/react @heroicons/react

# Form handling
npm install react-hook-form @hookform/resolvers zod

# Rich text editor (for notes)
npm install @tiptap/react @tiptap/starter-kit

# Date handling
npm install date-fns

# Drag and drop (for quests)
npm install @dnd-kit/core @dnd-kit/sortable
```

## Quick Wins (Do These First)

1. ✅ **Get it running** - Test with Docker
2. ✅ **Test API in Swagger** - Verify all endpoints work
3. 🔨 **Campaign List** - Fetch and display campaigns
4. 🔨 **Create Campaign Form** - Add new campaigns
5. 🔨 **Character List** - Show characters in campaign
6. 🔨 **Basic Navigation** - Link pages together

## Common Patterns

### API Hook Pattern
```typescript
// frontend/src/hooks/useResource.ts
export const useResource = (resource: string) => {
  return useQuery({
    queryKey: [resource],
    queryFn: async () => {
      const { data } = await api.get(`/${resource}`)
      return data
    }
  })
}
```

### Modal Pattern
```typescript
// frontend/src/components/Modal.tsx
export default function Modal({ isOpen, onClose, children }) {
  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white rounded-lg p-6 max-w-md w-full">
        {children}
      </div>
    </div>
  )
}
```

### Form Pattern
```typescript
// Using react-hook-form
import { useForm } from 'react-hook-form'

export default function CampaignForm({ onSubmit }) {
  const { register, handleSubmit, formState: { errors } } = useForm()

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('name', { required: true })} />
      {errors.name && <span>Name is required</span>}
      <button type="submit">Submit</button>
    </form>
  )
}
```

## Testing Strategy

1. **Manual Testing** - Test each feature in browser
2. **API Testing** - Use Swagger UI for backend
3. **Add Tests Later** - Focus on functionality first

## Need Help?

If you get stuck:
1. Check [API_EXAMPLES.md](API_EXAMPLES.md) for API usage
2. Check browser console for errors
3. Check backend logs: `docker-compose logs backend`
4. Test API directly in Swagger UI
5. Ask me for help with specific components!

## What Would You Like to Work On?

Pick one:
1. **Get it running** - I'll help you start the services and test
2. **Campaign List** - I'll build the campaign list with data fetching
3. **Character Sheet** - I'll create a character display component
4. **Custom feature** - Tell me what interests you most!

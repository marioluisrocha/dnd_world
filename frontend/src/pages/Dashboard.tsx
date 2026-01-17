import { Link } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'

export default function Dashboard() {
  const user = useAuthStore((state) => state.user)

  return (
    <div className="px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">
        Welcome back, {user?.username}!
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Link to="/campaigns" className="card hover:shadow-lg transition-shadow">
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Campaigns</h2>
          <p className="text-gray-600">
            Manage your D&D campaigns and adventures
          </p>
        </Link>

        <Link to="/characters" className="card hover:shadow-lg transition-shadow">
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Characters</h2>
          <p className="text-gray-600">
            Track player characters and NPCs
          </p>
        </Link>

        <Link to="/places" className="card hover:shadow-lg transition-shadow">
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Places</h2>
          <p className="text-gray-600">
            Document locations and world geography
          </p>
        </Link>

        <Link to="/items" className="card hover:shadow-lg transition-shadow">
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Items</h2>
          <p className="text-gray-600">
            Manage equipment and magic items
          </p>
        </Link>

        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Quick Stats</h2>
          <p className="text-gray-600">
            View your campaigns and sessions at a glance
          </p>
        </div>

        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-2">D&D Beyond</h2>
          <p className="text-gray-600">
            Import character sheets from D&D Beyond
          </p>
        </div>
      </div>
    </div>
  )
}

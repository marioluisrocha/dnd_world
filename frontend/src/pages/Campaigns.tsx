export default function Campaigns() {
  return (
    <div className="px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Campaigns</h1>
        <button className="btn btn-primary">
          Create Campaign
        </button>
      </div>

      <div className="card">
        <p className="text-gray-600">
          Your campaigns will appear here. Create your first campaign to get started!
        </p>
      </div>
    </div>
  )
}

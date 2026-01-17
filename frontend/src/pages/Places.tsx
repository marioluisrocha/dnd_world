export default function Places() {
  return (
    <div className="px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Places</h1>
        <button className="btn btn-primary">
          Add Place
        </button>
      </div>

      <div className="card">
        <p className="text-gray-600">
          Your world locations will appear here.
        </p>
      </div>
    </div>
  )
}

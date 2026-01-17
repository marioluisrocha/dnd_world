export default function Items() {
  return (
    <div className="px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Items</h1>
        <button className="btn btn-primary">
          Add Item
        </button>
      </div>

      <div className="card">
        <p className="text-gray-600">
          Your items and equipment will appear here.
        </p>
      </div>
    </div>
  )
}

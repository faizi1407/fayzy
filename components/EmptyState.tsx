export default function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center py-16 px-4">
      <div className="text-center">
        <svg 
          className="mx-auto h-24 w-24 text-gray-400" 
          fill="none" 
          viewBox="0 0 24 24" 
          stroke="currentColor"
        >
          <path 
            strokeLinecap="round" 
            strokeLinejoin="round" 
            strokeWidth={1.5} 
            d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" 
          />
        </svg>
        <h3 className="mt-6 text-2xl font-semibold text-gray-900">
          Coming Soon
        </h3>
        <p className="mt-2 text-gray-600 max-w-md mx-auto">
          We're preparing something delicious for you! Our chocolate varieties will be available soon.
        </p>
        <div className="mt-6">
          <button className="px-6 py-3 bg-amber-600 text-white rounded-md hover:bg-amber-700 transition-colors duration-200 font-medium">
            Notify Me
          </button>
        </div>
      </div>
    </div>
  );
}

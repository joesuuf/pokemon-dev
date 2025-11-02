interface SkeletonLoaderProps {
  isLoading: boolean
  itemCount?: number
}

export default function SkeletonLoader({ isLoading, itemCount = 3 }: SkeletonLoaderProps) {
  if (!isLoading) return null

  return (
    <div className="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-pulse">
      {Array.from({ length: itemCount }).map((_, idx) => (
        <div key={idx} className="bg-white rounded-lg shadow-lg overflow-hidden">
          {/* Image placeholder */}
          <div className="aspect-video bg-gray-300 rounded-t-lg" />

          {/* Content placeholder */}
          <div className="p-4">
            {/* Title */}
            <div className="h-6 bg-gray-300 rounded w-3/4 mb-2" />

            {/* Set info */}
            <div className="h-4 bg-gray-200 rounded w-1/2 mb-4" />

            {/* Prices section */}
            <div className="border-t border-gray-200 pt-3 mb-4">
              <div className="h-3 bg-gray-200 rounded w-1/4 mb-2" />
              <div className="space-y-2">
                <div className="h-4 bg-gray-300 rounded w-1/3" />
                <div className="h-4 bg-gray-300 rounded w-1/3" />
              </div>
            </div>

            {/* Buttons placeholder */}
            <div className="flex gap-2">
              <div className="flex-1 h-10 bg-gray-300 rounded" />
              <div className="flex-1 h-10 bg-gray-300 rounded" />
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

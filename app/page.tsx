import { Suspense } from 'react';
import { getMockProducts } from '@/lib/api';
import ProductGrid from '@/components/ProductGrid';
import ProductCardSkeleton from '@/components/ProductCardSkeleton';

export default async function Home() {
  const products = await getMockProducts();

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900">
            Fayzy Chocolate Collection
          </h1>
          <p className="mt-2 text-gray-600">
            Discover our finest selection of handcrafted chocolates
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Suspense fallback={
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {Array.from({ length: 8 }).map((_, index) => (
              <ProductCardSkeleton key={index} />
            ))}
          </div>
        }>
          <ProductGrid products={products} />
        </Suspense>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <p className="text-center text-gray-600">
            © 2024 Fayzy Chocolates. Crafted with love.
          </p>
        </div>
      </footer>
    </div>
  );
}

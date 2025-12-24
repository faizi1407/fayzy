import { Product } from '@/types/product';

// Configuration for API endpoint
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Fetch products from the FastAPI endpoint
 * This function is designed to be used in Server Components for optimal SEO
 */
export async function getProducts(): Promise<Product[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/products`, {
      // Revalidate every 60 seconds for ISR
      next: { revalidate: 60 }
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch products: ${response.statusText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching products:', error);
    // Return mock data as fallback for development
    return getMockProducts();
  }
}

/**
 * Mock products for development/testing
 */
export function getMockProducts(): Product[] {
  return [
    {
      id: '1',
      title: 'Dark Chocolate Truffles',
      price: 12.99,
      image: 'https://images.unsplash.com/photo-1511381939415-e44015466834?w=400&h=300&fit=crop',
      description: 'Rich and smooth dark chocolate truffles with 70% cocoa. Hand-crafted with premium Belgian chocolate.',
      category: 'truffles',
      stock: 25
    },
    {
      id: '2',
      title: 'Milk Chocolate Hearts',
      price: 9.99,
      image: 'https://images.unsplash.com/photo-1548848933-bfb1f9a88f86?w=400&h=300&fit=crop',
      description: 'Creamy milk chocolate hearts, perfect for gifting. Made with fresh cream and the finest cocoa beans.',
      category: 'hearts',
      stock: 30
    },
    {
      id: '3',
      title: 'White Chocolate Raspberry',
      price: 14.99,
      image: 'https://images.unsplash.com/photo-1481391243133-f96216dcb5d2?w=400&h=300&fit=crop',
      description: 'Delicate white chocolate infused with real raspberry puree. A sweet and tangy combination.',
      category: 'specialty',
      stock: 15
    },
    {
      id: '4',
      title: 'Hazelnut Praline',
      price: 16.99,
      image: 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=400&h=300&fit=crop',
      description: 'Crunchy hazelnut praline covered in smooth milk chocolate. Contains roasted hazelnuts from Italy.',
      category: 'pralines',
      stock: 20
    },
    {
      id: '5',
      title: 'Sea Salt Caramel',
      price: 13.99,
      image: 'https://images.unsplash.com/photo-1515037893149-de7f840978e2?w=400&h=300&fit=crop',
      description: 'Smooth caramel center with a hint of sea salt, covered in dark chocolate. A perfect balance of sweet and salty.',
      category: 'caramels',
      stock: 18
    },
    {
      id: '6',
      title: 'Mint Chocolate Squares',
      price: 10.99,
      image: 'https://images.unsplash.com/photo-1610450949065-1f2841536c88?w=400&h=300&fit=crop',
      description: 'Refreshing mint cream sandwiched between layers of dark chocolate. Cool and satisfying.',
      category: 'squares',
      stock: 22
    },
    {
      id: '7',
      title: 'Assorted Chocolate Box',
      price: 24.99,
      image: 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400&h=300&fit=crop',
      description: 'A curated selection of our finest chocolates. Contains 16 pieces of various flavors and styles.',
      category: 'boxes',
      stock: 12
    },
    {
      id: '8',
      title: 'Orange Zest Dark Chocolate',
      price: 11.99,
      image: 'https://images.unsplash.com/photo-1606312619070-d48b4cbc5b61?w=400&h=300&fit=crop',
      description: 'Dark chocolate infused with natural orange zest. Citrusy and sophisticated.',
      category: 'specialty',
      stock: 28
    }
  ];
}

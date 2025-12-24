# Fayzy Chocolate Collection

An interactive product catalog for browsing and exploring premium handcrafted chocolates. Built with Next.js 14, TypeScript, and Tailwind CSS.

## Features

- 🎨 **Interactive Product Grid**: Responsive grid layout displaying chocolate products with images, titles, and prices
- 🔍 **Product Details Modal**: Click "View Details" to see detailed product information without page reload
- 🏷️ **Category Filtering**: Filter products by category (Truffles, Hearts, Specialty, etc.)
- ⚡ **Skeleton Loaders**: Smooth loading states for better UX on slow connections
- 📦 **Empty State**: Graceful "Coming Soon" message when no products are available
- 🚀 **Performance Optimized**: Server Components for SEO, Client Components for interactivity
- 📱 **Fully Responsive**: Works seamlessly on mobile, tablet, and desktop

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the application.

### Build for Production

```bash
npm run build
npm start
```

## Project Structure

```
├── app/
│   ├── page.tsx              # Main products page (Server Component)
│   ├── layout.tsx            # Root layout
│   └── globals.css           # Global styles
├── components/
│   ├── ProductGrid.tsx       # Client Component - Grid with filtering
│   ├── ProductCard.tsx       # Product card component
│   ├── ProductModal.tsx      # Product details modal
│   ├── ProductCardSkeleton.tsx # Loading skeleton
│   └── EmptyState.tsx        # Empty state component
├── lib/
│   └── api.ts                # API functions and mock data
├── types/
│   └── product.ts            # TypeScript type definitions
└── public/                   # Static assets
```

## Architecture

- **Server Components**: Main page uses Next.js Server Components for optimal SEO and performance
- **Client Components**: Interactive elements (grid, modal, filters) use Client Components
- **API Integration**: Ready to connect to FastAPI backend via `NEXT_PUBLIC_API_URL` environment variable
- **Image Optimization**: Uses Next.js Image component for automatic optimization

## Environment Variables

Create a `.env.local` file to configure the API endpoint:

```env
NEXT_PUBLIC_API_URL=http://your-fastapi-backend:8000
```

## Performance

- Grid rendering: < 200ms after data fetch ✓
- Skeleton loaders on slow connections ✓
- Server-side rendering for SEO optimization ✓
- Image lazy loading and optimization ✓

## Future Enhancements

- Add to cart functionality
- Search functionality
- Product sorting options
- User authentication
- Wishlist feature

## License

MIT

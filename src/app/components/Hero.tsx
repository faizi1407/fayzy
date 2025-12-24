'use client';

import Image from 'next/image';
import { motion } from 'framer-motion';

export default function Hero() {
  return (
    <section className="relative w-full min-h-screen flex items-center justify-center overflow-hidden bg-gradient-to-br from-amber-50 via-orange-50 to-amber-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      {/* Container with fixed aspect ratio to prevent CLS */}
      <div className="relative w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-20">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12 items-center">
          
          {/* Text Content with Framer Motion animations */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, ease: 'easeOut' }}
            className="z-10 text-center lg:text-left order-2 lg:order-1"
          >
            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold text-gray-900 dark:text-white mb-6 leading-tight"
            >
              Premium
              <span className="block text-amber-700 dark:text-amber-400">
                Artisan Chocolate
              </span>
            </motion.h1>
            
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              className="text-lg sm:text-xl md:text-2xl text-gray-700 dark:text-gray-300 mb-8 max-w-xl mx-auto lg:mx-0"
            >
              Discover the rich, luxurious taste of handcrafted chocolate. 
              Made with the finest ingredients for an unforgettable experience.
            </motion.p>
            
            {/* CTA Button - Minimum 44x44px for touch targets */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.6 }}
              className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start"
            >
              <button
                className="inline-flex items-center justify-center px-8 py-4 min-w-[160px] min-h-[44px] text-lg font-semibold text-white bg-amber-700 rounded-lg shadow-lg hover:bg-amber-800 active:bg-amber-900 transition-all duration-200 transform hover:scale-105 focus:outline-none focus:ring-4 focus:ring-amber-500 focus:ring-opacity-50 dark:bg-amber-600 dark:hover:bg-amber-700"
                aria-label="Buy premium chocolate now"
              >
                Buy Now
              </button>
              
              <button
                className="inline-flex items-center justify-center px-8 py-4 min-w-[160px] min-h-[44px] text-lg font-semibold text-amber-700 bg-white border-2 border-amber-700 rounded-lg shadow-md hover:bg-amber-50 active:bg-amber-100 transition-all duration-200 focus:outline-none focus:ring-4 focus:ring-amber-500 focus:ring-opacity-50 dark:bg-gray-800 dark:text-amber-400 dark:border-amber-600 dark:hover:bg-gray-700"
                aria-label="Learn more about our chocolate"
              >
                Learn More
              </button>
            </motion.div>
          </motion.div>

          {/* Hero Image with Next/Image optimization */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, ease: 'easeOut' }}
            className="relative order-1 lg:order-2"
          >
            {/* Fixed aspect ratio container to prevent CLS - 16:9 ratio */}
            <div className="relative w-full aspect-[4/3] lg:aspect-square max-w-2xl mx-auto">
              <div className="absolute inset-0 bg-gradient-to-br from-amber-200/20 to-orange-300/20 rounded-2xl transform rotate-3" />
              <div className="absolute inset-0 bg-gradient-to-tl from-amber-300/10 to-orange-200/10 rounded-2xl transform -rotate-3" />
              
              <div className="relative w-full h-full rounded-2xl overflow-hidden shadow-2xl">
                <Image
                  src="/chocolate-hero.jpg"
                  alt="Premium artisan chocolate bars with rich cocoa"
                  fill
                  priority
                  sizes="(max-width: 768px) 100vw, (max-width: 1024px) 50vw, 600px"
                  className="object-cover"
                  style={{ objectPosition: 'center' }}
                />
              </div>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Decorative background elements */}
      <div className="absolute top-20 left-10 w-72 h-72 bg-amber-300/10 rounded-full blur-3xl" />
      <div className="absolute bottom-20 right-10 w-96 h-96 bg-orange-400/10 rounded-full blur-3xl" />
    </section>
  );
}

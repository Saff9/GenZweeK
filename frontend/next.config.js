// frontend/next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**',
      },
    ],
  },
  // TEMPORARILY DISABLE rewrites until backend is live
  async rewrites() {
    return process.env.NEXT_PUBLIC_API_BASE 
      ? [{
          source: '/api/:path*',
          destination: `${process.env.NEXT_PUBLIC_API_BASE}/:path*`,
        }]
      : []
  },
}

module.exports = nextConfig

/** @type {import('next').NextConfig} */
// const {createProxyMiddleware} = require('http-proxy-middleware');

const nextConfig = {
  reactStrictMode: false,
  experimental: {
    urlImports: ['https://esm.sh', 'https://cdn.jsdelivr.net'],
  },
  async rewrites() {
    return [
      {
        source: '/server/:path*',
        destination: 'http://localhost:8088/:path*', // Proxy all requests to localhost:8088
      },
    ];
  },
}

module.exports = nextConfig

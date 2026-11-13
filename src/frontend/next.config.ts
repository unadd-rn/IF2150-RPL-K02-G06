import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  experimental: {
    agentFeedback: true,
  },
    async rewrites() {
    return [
      {
        // Semua request /api/* diteruskan ke FastAPI (same-origin, agar cookie sesi ikut terkirim).
        // Sudah mencakup /api/pembayaran/scan/:token untuk demo QR.
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ];
  },
  cacheComponents: true,
  partialPrefetching: true,
  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },
};

export default nextConfig;

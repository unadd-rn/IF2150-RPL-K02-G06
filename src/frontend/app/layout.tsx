import type { Metadata } from "next";
import type { ReactNode } from "react";
import { Suspense } from "react";
// Hanya muat subset latin: 400.css/700.css penuh berisi ~240 file font Jepang
// (~33MB) yang membuat dev server sangat lambat.
import "@fontsource/line-seed-jp/latin-400.css";
import "@fontsource/line-seed-jp/latin-700.css";
import { CartProvider } from "@/lib/cart";
import { ThemeSync } from "@/components/ThemeSync";
import "./globals.css";

export const metadata: Metadata = {
  title: "SaveBite",
  description: "SaveBite mobile-first food surplus marketplace",
};

export default function RootLayout({ children }: Readonly<{ children: ReactNode }>) {
  return (
    <html
      lang="en"
      className="h-full antialiased"
    >
      <body className="min-h-screen bg-[#0d1d27] text-[#171717]">
        <Suspense fallback={null}>
          <ThemeSync />
        </Suspense>
        <CartProvider>{children}</CartProvider>
      </body>
    </html>
  );
}

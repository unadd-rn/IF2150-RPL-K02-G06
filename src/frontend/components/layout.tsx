"use client";

import type { ReactNode } from "react";
import { BottomNavbar, buildNavItems, type NavItem, type UserRole } from "@/components/bottom-navbar";

export interface AppLayoutProps {
  children: ReactNode;
  title?: ReactNode; // Updated from string to ReactNode
  subtitle?: string;
  role?: UserRole;
  isAuthenticated?: boolean;
  showHeader?: boolean;
  showBottomNav?: boolean;
  navItems?: NavItem[];
  className?: string;
  headerClassName?: string;
  bodyClassName?: string;
  /** Tema warna header halaman: ikut animasi fade antar halaman. */
  theme?: "green" | "blue" | "pink";
}

export function AppLayout({
  children,
  title,
  subtitle,
  role = "buyer",
  isAuthenticated = true,
  showHeader = true,
  showBottomNav = true,
  navItems,
  className = "",
  headerClassName = "",
  bodyClassName = "",
  theme,
}: AppLayoutProps) {
  const resolvedNavItems = navItems ?? buildNavItems({ role, isAuthenticated });

  return (
    <div className="min-h-screen bg-[#e6e0c8]">
      <div className="flex min-h-screen w-full flex-col overflow-hidden bg-[#e6e0c8]">
        {showHeader && (
          <header
            className={`px-5 pb-5 pt-7 text-[#fff4f2] sm:px-6 lg:px-8 ${headerClassName} ${
              theme ? "themed-header" : headerClassName ? "" : "bg-[#f56369]"
            }`}
          >
            {title ? (
              typeof title === "string" ? (
                <h1 className="text-3xl font-black tracking-[-0.06em] text-[#fff4f2] sm:text-4xl lg:text-5xl">
                  {title}
                </h1>
              ) : (
                // If it's a React element (like an Image), render it directly without forcing an <h1>
                title
              )
            ) : null}
            {subtitle ? <p className="mt-2 text-sm opacity-90">{subtitle}</p> : null}
          </header>
        )}

        {/* pb besar: jarak konsisten antara konten terakhir & bottom navbar (fixed) di semua halaman. */}
        <main className={`flex-1 bg-[#e6e0c8] pb-24 ${bodyClassName} ${className}`}>
          {children}
        </main>

        {showBottomNav ? <BottomNavbar items={resolvedNavItems} className="fixed inset-x-0 bottom-0 z-50" /> : null}
      </div>
    </div>
  );
}
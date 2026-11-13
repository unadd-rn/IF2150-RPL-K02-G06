"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Suspense, type JSX } from "react";
import { useCart } from "@/lib/cart";

export type UserRole = "guest" | "buyer" | "seller";

export interface NavItem {
  id: string;
  label: string;
  href: string;
  icon: JSX.Element;
  roles?: UserRole[];
}

const buyerItems: Omit<NavItem, "roles">[] = [
  {
    id: "home",
    label: "Home",
    href: "/katalog",
    icon: <HomeIcon />,
  },
  {
    id: "cart",
    label: "Cart",
    href: "/cart",
    icon: <CartIcon />,
  },
  {
    id: "reward",
    label: "Account",
    href: "/reward",
    icon: <AccountIcon />,
  },
];

const sellerItems: Omit<NavItem, "roles">[] = [
  {
    id: "dashboard",
    label: "Home",
    href: "/penjual",
    icon: <HomeIcon />,
  },
  {
    id: "listings",
    label: "Listings",
    href: "/penjual/listing",
    icon: <ListIcon />,
  },
  {
    id: "account",
    label: "Account",
    href: "/penjual/account",
    icon: <AccountIcon />,
  },
];

export function buildNavItems(options: {
  role: UserRole;
  isAuthenticated: boolean;
}): NavItem[] {
  const effectiveRole: UserRole = options.isAuthenticated ? options.role : "guest";

  const sourceItems = effectiveRole === "seller" ? sellerItems : buyerItems;

  return sourceItems.map((item) => ({
    ...item,
    roles: [effectiveRole],
  }));
}

interface BottomNavbarProps {
  items: NavItem[];
  className?: string;
}

export function BottomNavbar({ items, className = "" }: BottomNavbarProps) {
  return (
    <Suspense fallback={<NavbarFallback className={className} />}> 
      <BottomNavbarContent items={items} className={className} />
    </Suspense>
  );
}

function BottomNavbarContent({ items, className = "" }: BottomNavbarProps) {
  const pathname = usePathname();
  const { siap, totalItem } = useCart();

  return (
    <nav
      aria-label="Primary navigation"
      className={`themed-nav border-t px-3 py-2 ${className}`}
    >
      <ul className="flex items-center justify-between gap-2">
        {items.map((item) => {
          const isActive =
            pathname === item.href ||
            (item.href !== "/" && pathname.startsWith(item.href));

          return (
            <li key={item.id} className="flex-1">
              <Link
                href={item.href}
                className={`flex flex-col items-center justify-center gap-1 rounded-xl px-2 py-2 text-[0.7rem] font-medium transition-colors ${
                  isActive
                    ? "text-white focus-visible:text-white"
                    : "text-[var(--theme-nav-inactive)] opacity-90 hover:text-white focus-visible:text-white"
                }`}
                aria-current={isActive ? "page" : undefined}
                aria-label={
                  item.id === "cart" && siap && totalItem > 0
                    ? `Cart, ${totalItem} item`
                    : undefined
                }
              >
                <span
                  className={`relative flex h-7 w-7 items-center justify-center ${
                    isActive ? "scale-110" : ""
                  }`}
                >
                  {item.icon}
                  {item.id === "cart" && siap && totalItem > 0 && (
                    <span
                      data-testid="cart-badge"
                      className="absolute -right-2 -top-1.5 flex h-[1.15rem] min-w-[1.15rem] items-center justify-center rounded-full bg-[#f25f4b] px-1 text-[0.65rem] font-bold text-white"
                    >
                      {totalItem > 99 ? "99+" : totalItem}
                    </span>
                  )}
                </span>
                <span>{item.label}</span>
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}

function NavbarFallback({ className = "" }: { className?: string }) {
  return (
    <nav
      aria-label="Primary navigation"
      className={`themed-nav border-t px-3 py-2 ${className}`}
    >
      <ul className="flex items-center justify-between gap-2">
        {["Home", "Cart", "Account"].map((label) => (
          <li key={label} className="flex-1">
            <div className="flex flex-col items-center justify-center gap-1 rounded-xl px-2 py-2 text-[0.7rem] font-medium text-[var(--theme-nav-inactive)] opacity-90">
              <span className="flex h-7 w-7 items-center justify-center">•</span>
              <span>{label}</span>
            </div>
          </li>
        ))}
      </ul>
    </nav>
  );
}

function HomeIcon() {
  return (
    <svg viewBox="0 0 24 24" className="h-6 w-6 fill-none stroke-current stroke-[1.8]" aria-hidden="true">
      <path d="M3 10.5 12 3l9 7.5" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M5 9.5V20h14V9.5" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

function CartIcon() {
  return (
    <svg viewBox="0 0 24 24" className="h-6 w-6 fill-none stroke-current stroke-[1.8]" aria-hidden="true">
      <circle cx={9} cy={18} r={1.8} />
      <circle cx={17} cy={18} r={1.8} />
      <path d="M3 4h2l2.2 9.2a1 1 0 0 0 1 .8h8.9a1 1 0 0 0 1-.8L19 7H7" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

function AccountIcon() {
  return (
    <svg viewBox="0 0 24 24" className="h-6 w-6 fill-none stroke-current stroke-[1.8]" aria-hidden="true">
      <circle cx={12} cy={8} r={4} />
      <path d="M5 19c1.6-2.6 4.2-4 7-4s5.4 1.4 7 4" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

function ListIcon() {
  return (
    <svg viewBox="0 0 24 24" className="h-6 w-6 fill-none stroke-current stroke-[1.8]" aria-hidden="true">
      <path d="M8 6h11M8 12h11M8 18h11M3 6h.01M3 12h.01M3 18h.01" strokeLinecap="round" />
    </svg>
  );
}

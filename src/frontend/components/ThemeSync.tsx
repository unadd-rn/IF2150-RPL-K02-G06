"use client";

import { useLayoutEffect, useRef } from "react";
import { usePathname } from "next/navigation";

interface TemaHalaman {
  header: string;
  nav: string;
  navBorder: string;
  navInactive: string;
}

/** Tema default di luar halaman bertema (detail penjual, login, dll.). */
const TEMA_DEFAULT: TemaHalaman = {
  header: "#f56369",
  nav: "#1ab0c7",
  navBorder: "rgba(42, 142, 161, 0.3)",
  navInactive: "#d8faff",
};

/** Halaman Home (katalog dan detail listing di dalamnya). */
const TEMA_HIJAU: TemaHalaman = {
  header: "#1EA96A",
  nav: "#1EA96A",
  navBorder: "rgba(16, 110, 72, 0.35)",
  navInactive: "#DDF8E8",
};

/** Halaman Cart. */
const TEMA_BIRU: TemaHalaman = {
  header: "#1C8CC9",
  nav: "#1C8CC9",
  navBorder: "rgba(18, 82, 145, 0.35)",
  navInactive: "#DDECF9",
};

/** Halaman Account. */
const TEMA_PINK: TemaHalaman = {
  header: "#F56D7A",
  nav: "#F56D7A",
  navBorder: "rgba(156, 71, 81, 0.35)",
  navInactive: "#FFE2E6",
};

function temaUntukPath(pathname: string): TemaHalaman {
  if (pathname === "/" || pathname.startsWith("/katalog")) return TEMA_HIJAU;
  if (pathname.startsWith("/cart")) return TEMA_BIRU;
  if (pathname.startsWith("/reward") || pathname.startsWith("/penjual/account")) return TEMA_PINK;
  // Halaman penjual: dashboard ikut tema hijau; kelola/tambah/edit listing biru seperti Cart pembeli.
  if (pathname === "/penjual") return TEMA_HIJAU;
  if (pathname.startsWith("/penjual/listing")) return TEMA_BIRU;
  return TEMA_DEFAULT;
}

/**
 * Menyetel variabel CSS warna tema sesuai rute aktif. Dipasang sekali di root
 * layout sehingga tetap hidup antar navigasi dan warna bisa mem-fade dari
 * warna halaman sebelumnya (lihat .themed-header / .themed-nav di globals.css).
 */
export function ThemeSync() {
  const pathname = usePathname();
  const temaSebelumnya = useRef<TemaHalaman>(TEMA_DEFAULT);

  useLayoutEffect(() => {
    const temaBerikutnya = temaUntukPath(pathname);
    const style = document.documentElement.style;

    style.setProperty("--theme-header-from", temaSebelumnya.current.header);
    style.setProperty("--theme-header", temaBerikutnya.header);
    style.setProperty("--theme-nav-from", temaSebelumnya.current.nav);
    style.setProperty("--theme-nav", temaBerikutnya.nav);
    style.setProperty("--theme-nav-border-from", temaSebelumnya.current.navBorder);
    style.setProperty("--theme-nav-border", temaBerikutnya.navBorder);
    style.setProperty("--theme-nav-inactive", temaBerikutnya.navInactive);

    temaSebelumnya.current = temaBerikutnya;
  }, [pathname]);

  return null;
}

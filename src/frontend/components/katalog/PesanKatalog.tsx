import Link from "next/link";
import type { ReactNode } from "react";
import { ApiError } from "@/lib/api";

/** tampilkanPesan: pesan informasi atau kesalahan di KatalogView. */
export default function PesanKatalog({ children, jenis = "info" }: { children: ReactNode; jenis?: "info" | "error" }) {
  const warna =
    jenis === "error"
      ? "border-red-200 bg-red-50 text-red-700 dark:border-red-900 dark:bg-red-950 dark:text-red-300"
      : "border-zinc-200 bg-zinc-50 text-zinc-600 dark:border-zinc-800 dark:bg-zinc-900 dark:text-zinc-400";
  return (
    <p role={jenis === "error" ? "alert" : "status"} className={`rounded-lg border px-4 py-3 text-sm ${warna}`}>
      {children}
    </p>
  );
}

/** 401/403 dari require_roles P1 → minta login ulang sebagai pembeli. */
export function perluLogin(e: unknown): boolean {
  return e instanceof ApiError && (e.status === 401 || e.status === 403);
}

export function PesanPerluLogin() {
  return (
    <PesanKatalog jenis="error">
      Your session is invalid or is not a customer account.{" "}
      <Link href="/login" className="font-medium underline">
        Log in as a customer
      </Link>
    </PesanKatalog>
  );
}

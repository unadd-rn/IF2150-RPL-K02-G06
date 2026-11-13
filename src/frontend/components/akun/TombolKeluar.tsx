"use client";

// Tombol keluar untuk halaman akun (/reward).
// Alur: POST /api/auth/logout menghapus sesi di server + cookie httpOnly,
// keranjang milik sesi diosongkan, lalu alih ke halaman login.
import { useState } from "react";
import { useRouter } from "next/navigation";
import { ApiError, logoutSesi } from "@/lib/api";
import { useCart } from "@/lib/cart";

export default function TombolKeluar() {
  const router = useRouter();
  const { kosongkan } = useCart();
  const [sedangKeluar, setSedangKeluar] = useState(false);
  const [pesan, setPesan] = useState<string | null>(null);

  async function keluar() {
    setSedangKeluar(true);
    setPesan(null);
    try {
      await logoutSesi();
      kosongkan(); // isi keranjang milik sesi yang baru saja berakhir
      router.replace("/login");
    } catch (error) {
      setSedangKeluar(false);
      setPesan(
        error instanceof ApiError ? error.message : "Could not log out. Please try again.",
      );
    }
  }

  return (
    <div className="space-y-2 text-center">
      <button
        type="button"
        onClick={keluar}
        disabled={sedangKeluar}
        className="w-full rounded-[18px] bg-[#f56068] px-4 py-3 text-base font-bold text-white shadow-sm transition-opacity hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-60"
        aria-label="Log out of account"
      >
        {sedangKeluar ? "Logging out…" : "Log out"}
      </button>
      {pesan && (
        <p className="text-sm font-medium text-[#f15a62]" role="alert">
          {pesan}
        </p>
      )}
    </div>
  );
}

"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { ambilDetailKatalog, ApiError, type ListingKatalog } from "@/lib/api";
import DaftarListing from "./DaftarListing";
import EmptyState from "./EmptyState";
import FotoListing from "./FotoListing";
import PesanKatalog, { perluLogin, PesanPerluLogin } from "./PesanKatalog";
import PengaturJumlah from "./PengaturJumlah";
import { formatRupiah, formatWaktu } from "./format";
import NotifikasiGagal from "@/components/NotifikasiGagal";

function StoreIcon({ className = "" }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" className={className} fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M3 9.5 4.5 4h15L21 9.5" />
      <path d="M3 9.5h18v2a3 3 0 0 1-6 0 3 3 0 0 1-6 0 3 3 0 0 1-6 0v-2Z" />
      <path d="M5 12.6V20h14v-7.4" />
    </svg>
  );
}

type State =
  | { untukId: string; status: "ok"; listing: ListingKatalog }
  | { untukId: string; status: "error"; pesan: string; tidakTersedia: boolean }
  | { untukId: string; status: "perluLogin" };

/** pilihListing + tampilkanDetail (Algo-C11-02, UC03). */
export default function DetailListing() {
  const { id } = useParams<{ id: string }>();
  const [hasil, setHasil] = useState<State | null>(null);
  const [notifikasi, setNotifikasi] = useState<string | null>(null);
  // Hasil milik id lain (mis. pindah listing) dianggap masih memuat
  const state = hasil?.untukId === id ? hasil : { status: "memuat" as const };

  useEffect(() => {
    let aktif = true;
    ambilDetailKatalog(id)
      .then((listing) => aktif && setHasil({ untukId: id, status: "ok", listing }))
      .catch((e) => {
        if (!aktif) return;
        if (perluLogin(e)) return setHasil({ untukId: id, status: "perluLogin" });
        const status = e instanceof ApiError ? e.status : 0;
        setHasil({
          untukId: id,
          status: "error",
          pesan: status === 404 || status === 422 ? "This listing is no longer available" : e instanceof ApiError ? e.message : "Could not load listing details",
          tidakTersedia: status === 404 || status === 422,
        });
        if (status === 404 || status === 422) setNotifikasi("This listing is no longer available because it is out of stock, inactive, deleted, or past its expiration date.");
      });
    return () => {
      aktif = false;
    };
  }, [id]);

  if (state.status === "memuat") return <PesanKatalog>Loading listing details…</PesanKatalog>;
  if (state.status === "perluLogin") return <PesanPerluLogin />;

  if (state.status === "error") {
    if (!state.tidakTersedia) return <PesanKatalog jenis="error">{state.pesan}</PesanKatalog>;
    // UC03 Alt 1 (Algo-C11-02): listing sudah dihapus/habis → pesan, lalu kembali ke daftar listing
    return (
      <>
      <NotifikasiGagal pesan={notifikasi} onClose={() => setNotifikasi(null)} />
      <div className="flex flex-col gap-6">
        <EmptyState jenis="error" judul={state.pesan} aksi={{ href: "/katalog", label: "Back to catalog" }}>
          The seller may have deleted this listing, it may be out of stock, or it may have passed its expiration date.
        </EmptyState>
        <section className="flex flex-col gap-4">
          <h2 className="text-lg font-semibold">Other available surplus food</h2>
          <DaftarListing />
        </section>
      </div>
      </>
    );
  }

  const { listing } = state;
  return (
    <article className="flex flex-col gap-6 md:flex-row">
      <FotoListing foto={listing.foto} alt={listing.nama_makanan} className="aspect-[4/3] w-full rounded-xl md:w-1/2" />
      <div className="flex flex-1 flex-col gap-4">
        <div>
          <h1 className="text-2xl font-bold">{listing.nama_makanan}</h1>
          <p className="mt-1 text-2xl font-bold text-emerald-700 dark:text-emerald-400">{formatRupiah(listing.harga)}</p>
        </div>
        {listing.deskripsi && <p className="text-[#0a8ea8] dark:text-[#0a8ea8]">{listing.deskripsi}</p>}
        {/* Toko penjual + lokasi pengambilan makanan (R09: pickup di tempat) */}
        <div className="rounded-xl border border-[#d7cfb5] bg-[#f7f0dc] p-4 text-sm">
          <p className="inline-flex items-center gap-1.5 font-bold text-[#0a8ea8]">
            <StoreIcon className="h-4 w-4" aria-hidden="true" />
            {listing.nama_toko}
          </p>
          <p className="mt-1.5 text-zinc-600 dark:text-zinc-400">
            <span className="font-semibold text-[#264b4d]">Pickup location:</span>{" "}
            {listing.alamat_toko || "Store location unavailable"}
          </p>
        </div>
        <dl className="grid grid-cols-[auto_1fr] gap-x-6 gap-y-2 text-sm">
          <dt className="text-zinc-500">Serving</dt>
          <dd>{listing.porsi}</dd>
          <dt className="text-zinc-500">Condition</dt>
          <dd>{listing.kondisi === "Sangat Baik" ? "Excellent" : listing.kondisi === "Baik" ? "Good" : listing.kondisi === "Layak Konsumsi" ? "Safe to Eat" : listing.kondisi}</dd>
          <dt className="text-zinc-500">Stock</dt>
          <dd>{listing.stok}</dd>
          <dt className="text-zinc-500">Expiration date</dt>
          <dd>{formatWaktu(listing.batas_kedaluwarsa)}</dd>
        </dl>
        <div className="flex flex-wrap items-center gap-4 pt-2">
          {/* Adjust quantity here; checkout continues through the cart. */}
          <PengaturJumlah listing={listing} ukuran="besar" />
          <Link href="/cart" className="text-sm text-[#0a8ea8] underline hover:text-[#0d7b96]">
            View cart
          </Link>
          <Link href="/katalog" className="text-sm text-zinc-600 underline dark:text-zinc-400">
            Back to catalog
          </Link>
        </div>
      </div>
    </article>
  );
}

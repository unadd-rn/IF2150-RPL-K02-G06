"use client";

import Link from "next/link";
import type { ListingKatalog } from "@/lib/api";
import PengaturJumlah from "./PengaturJumlah";
import FotoListing from "./FotoListing";
import { formatRupiah } from "./format";

function StoreIcon({ className = "" }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" className={className} fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M3 9.5 4.5 4h15L21 9.5" />
      <path d="M3 9.5h18v2a3 3 0 0 1-6 0 3 3 0 0 1-6 0 3 3 0 0 1-6 0v-2Z" />
      <path d="M5 12.6V20h14v-7.4" />
    </svg>
  );
}

export default function KartuListing({ listing }: { listing: ListingKatalog }) {
  // Mobile: kartu horizontal ringkas (foto di kiri, info di kanan).
  // Layar lebih lebar (sm+): tetap kartu vertikal seperti sebelumnya.
  return (
    <article className="group flex h-full items-stretch gap-3 overflow-hidden rounded-[16px] border border-[#d7cfb5] bg-[#f7f0dc] p-3 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md sm:flex-col sm:items-stretch sm:gap-0 sm:rounded-[18px]">
      <Link
        href={`/katalog/${listing.id_listing}`}
        className="block shrink-0"
        aria-label={`View details for ${listing.nama_makanan}`}
      >
        {/* Rasio foto dikunci di container (4/3) supaya semua kartu punya tinggi sama,
            dan crop-nya konsisten antara mobile & desktop. */}
        <div className="h-full w-24 overflow-hidden rounded-[12px] border border-[#d7cfb5] bg-[#f5d7aa] sm:aspect-[4/3] sm:h-auto sm:w-full sm:rounded-[14px]">
          <FotoListing
            foto={listing.foto}
            alt={listing.nama_makanan}
            className="h-full w-full object-cover"
          />
        </div>
      </Link>

      <div className="flex min-w-0 flex-1 flex-col justify-between gap-2 sm:mt-3 sm:gap-0">
        <Link href={`/katalog/${listing.id_listing}`} className="block min-w-0">
          <h2 className="line-clamp-2 text-base font-extrabold leading-snug tracking-[-0.02em] text-[#0a8ea8] group-hover:text-[#0d7b96] sm:text-[1.1rem] sm:tracking-[-0.04em]">
            {listing.nama_makanan}
          </h2>
          <p className="mt-0.5 line-clamp-1 text-xs leading-snug text-[#5c6460] sm:mt-1 sm:line-clamp-2 sm:text-sm">
            {listing.deskripsi || "Food surplus available now"}
          </p>
          <div className="mt-1.5 rounded-lg bg-[#e0ece9] px-2 py-1 sm:mt-2 sm:px-2.5 sm:py-2">
            <p className="flex items-center gap-1 text-[11px] font-semibold text-[#2a6a5b] sm:gap-1.5 sm:text-xs">
              <StoreIcon className="h-3 w-3 shrink-0 sm:h-3.5 sm:w-3.5" aria-hidden="true" />
              <span className="truncate">{listing.nama_toko}</span>
            </p>
            <p className="line-clamp-1 text-[10px] leading-snug text-[#4e5f56] sm:mt-1 sm:line-clamp-2 sm:text-xs">
              {listing.alamat_toko || "Store location unavailable"}
            </p>
          </div>
        </Link>

        <div className="flex items-end justify-between gap-2 sm:mt-auto sm:items-center sm:pt-3 sm:gap-3">
          <div className="min-w-0">
            <p className="text-base font-extrabold leading-tight text-[#1a1a1a] sm:text-lg">
              {formatRupiah(listing.harga)}
            </p>
            <p className="text-[10px] font-semibold uppercase tracking-[0.08em] text-[#5e6a61] sm:hidden">
              stok {listing.stok}
            </p>
          </div>

          <div className="flex shrink-0 items-center gap-2">
            <span className="hidden text-xs font-semibold uppercase tracking-[0.08em] text-[#5e6a61] sm:inline">
              stok {listing.stok}
            </span>
            {/* Pengatur jumlah di luar Link: klik +/− tidak boleh ikut membuka halaman detail. */}
            <div className="scale-90 origin-right sm:scale-100">
              <PengaturJumlah listing={listing} />
            </div>
          </div>
        </div>
      </div>
    </article>
  );
}

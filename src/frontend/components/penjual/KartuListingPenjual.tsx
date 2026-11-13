"use client";

import { ListingPenjual, urlFoto } from "@/lib/api";

export type ListingMakananPenjual = ListingPenjual;

interface KartuListingPenjualProps {
  listing: ListingMakananPenjual;
  onEdit: (id: number) => void;
  onHapus: (listing: ListingMakananPenjual) => void;
}

export default function KartuListingPenjual({
  listing,
  onEdit,
  onHapus,
}: KartuListingPenjualProps) {
  const fotoUrl = urlFoto(listing.foto);

  return (
    <div className="group flex h-full items-stretch gap-3 overflow-hidden rounded-[16px] border border-[#d8cfb4] bg-[#f7f0dc] p-3 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md sm:flex-col sm:gap-0 sm:rounded-[18px]">
      {/* Mobile: foto kecil di kiri; sm+: foto besar di atas seperti kartu pembeli. */}
      <div className="h-full w-24 shrink-0 overflow-hidden rounded-[12px] border border-[#d8cfb4] bg-[#f4d7ab] sm:aspect-[4/3] sm:h-auto sm:w-full sm:rounded-[14px]">
        {fotoUrl ? (
          <img
            src={fotoUrl}
            alt={listing.nama_makanan}
            className="h-full w-full object-cover"
          />
        ) : (
          <div className="flex h-full items-center justify-center text-[10px] text-[#5d655f] sm:text-xs">
            No photo
          </div>
        )}
      </div>

      <div className="flex min-w-0 flex-1 flex-col sm:mt-3">
        <div className="flex items-start justify-between gap-2">
          <h3 className="line-clamp-2 text-base font-extrabold leading-snug tracking-[-0.02em] text-[#0b8ea8] sm:text-[1.2rem] sm:tracking-[-0.04em]">
            {listing.nama_makanan}
          </h3>
          <button
            type="button"
            onClick={() => onHapus(listing)}
            className="shrink-0 text-xl font-black leading-none text-[#ef5a61] sm:text-2xl"
            aria-label={`Delete ${listing.nama_makanan}`}
          >
            ×
          </button>
        </div>

        <p className="mt-0.5 truncate text-xs leading-snug text-[#58635b] sm:mt-1 sm:text-sm">
          {listing.porsi} · {listing.kondisi === "Sangat Baik" ? "Excellent" : listing.kondisi === "Baik" ? "Good" : listing.kondisi === "Layak Konsumsi" ? "Safe to Eat" : listing.kondisi}
        </p>

        <div className="mt-1 flex items-baseline justify-between gap-3 sm:mt-3">
          <p className="text-base font-extrabold text-[#1a1a1a] sm:text-lg">
            Rp. {listing.harga.toLocaleString("id-ID")}
          </p>

          <p className="text-xs font-semibold text-[#58635b] sm:text-sm">
            Stock: {listing.stok}
          </p>
        </div>

        <div className="mt-auto flex items-center justify-between gap-2 border-t border-[#d9d1b5] pt-2 sm:mt-4 sm:pt-3">
          <span
            className={`rounded-full px-2.5 py-1 text-[0.7rem] font-bold uppercase ${
              listing.tersedia
                ? "bg-green-100 text-green-700"
                : "bg-red-100 text-red-700"
            }`}
          >
            {listing.draft ? "Draft" : listing.tersedia ? "Available" : "Unavailable"}
          </span>

          <button
            type="button"
            onClick={() => onEdit(listing.id_listing)}
            className="rounded-md border border-[#d6cfb6] bg-white px-3 py-2 text-sm font-medium text-[#496864] hover:bg-[#f3efe6]"
          >
            Edit
          </button>
        </div>
      </div>
    </div>
  );
}

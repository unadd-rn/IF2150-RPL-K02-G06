"use client";

export interface ListingMakananPenjual {
  id_listing: number;
  nama_makanan: string;
  porsi: string;
  kondisi: string;
  harga: number;
  stok: number;
  batas_kedaluwarsa: string;
  foto?: string | null;
  aktif: boolean;
}

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
  const isExpired = new Date(listing.batas_kedaluwarsa) <= new Date();

  return (
    <div className="flex flex-col overflow-hidden rounded-[18px] border border-[#d8cfb4] bg-[#f7f0dc] p-3 shadow-sm">
      <div className="flex items-start justify-between gap-3">
        <div className="relative h-[90px] w-[112px] overflow-hidden rounded-xl border border-[#d8cfb4] bg-[#f4d7ab]">
          {listing.foto ? (
            <img
              src={`http://localhost:8000${listing.foto}`}
              alt={listing.nama_makanan}
              className="h-full w-full object-cover"
            />
          ) : (
            <div className="flex h-full items-center justify-center text-xs text-[#5d655f]">No photo</div>
          )}
        </div>

        <button
          type="button"
          onClick={() => onHapus(listing)}
          className="text-2xl font-black text-[#ef5a61]"
          aria-label={`Delete ${listing.nama_makanan}`}
        >
          ×
        </button>
      </div>

      <div className="mt-3 flex-1">
        <h3 className="text-[1.2rem] font-extrabold tracking-[-0.04em] text-[#0b8ea8]">
          {listing.nama_makanan}
        </h3>
        <p className="mt-1 text-sm text-[#58635b]">{listing.porsi} · {listing.kondisi}</p>

        <div className="mt-3 flex items-center justify-between gap-3">
          <p className="text-lg font-extrabold text-[#1a1a1a]">
            Rp. {listing.harga.toLocaleString("id-ID")}
          </p>

          <div className="flex items-center">
            <button
              type="button"
              className="flex h-8 w-8 items-center justify-center rounded-l-md bg-[#ff4d57] text-lg font-bold text-white"
              aria-label={`Decrease stock for ${listing.nama_makanan}`}
            >
              −
            </button>
            <span className="flex h-8 w-9 items-center justify-center bg-[#ff4d57] text-sm font-bold text-white">
              {listing.stok}
            </span>
            <button
              type="button"
              className="flex h-8 w-8 items-center justify-center rounded-r-md bg-[#ff4d57] text-lg font-bold text-white"
              aria-label={`Increase stock for ${listing.nama_makanan}`}
            >
              +
            </button>
          </div>
        </div>
      </div>

      <div className="mt-4 flex items-center justify-between gap-2 border-t border-[#d9d1b5] pt-3">
        <span
          className={`rounded-full px-2.5 py-1 text-[0.7rem] font-bold uppercase ${
            listing.aktif && listing.stok > 0 && !isExpired
              ? "bg-green-100 text-green-700"
              : "bg-red-100 text-red-700"
          }`}
        >
          {listing.aktif && listing.stok > 0 && !isExpired ? "Tersedia" : "Tidak Tersedia"}
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
  );
}

"use client";

import FotoListing from "@/components/katalog/FotoListing";
import { formatRupiah, formatWaktu } from "@/components/katalog/format";
import type { PesananPenjual } from "@/lib/api";

interface KartuPesananPenjualProps {
  pesanan: PesananPenjual;
  isMenandai: boolean;
  onTandaiDiambil: (idTransaksi: number) => void;
}

export default function KartuPesananPenjual({
  pesanan,
  isMenandai,
  onTandaiDiambil,
}: KartuPesananPenjualProps) {
  const sudahDiambil = pesanan.waktu_diambil !== null;

  return (
    <div className="flex flex-col rounded-[18px] border border-[#d8cfb4] bg-[#f7f0dc] p-4 shadow-sm">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-semibold text-[#60756b]">
            Order #{pesanan.id_transaksi} · {formatWaktu(pesanan.tanggal)}
          </p>
          <p className="mt-1 text-xs font-semibold uppercase tracking-[0.08em] text-[#60756b]">
            Pickup code: {pesanan.kode_pengambilan ?? "-"}
          </p>
        </div>

        <span
          className={`shrink-0 rounded-full px-2.5 py-1 text-[0.7rem] font-bold uppercase ${
            sudahDiambil
              ? "bg-zinc-200 text-zinc-600"
              : "bg-green-100 text-green-700"
          }`}
        >
          {sudahDiambil ? "Complete" : "Ready for Pickup"}
        </span>
      </div>

      <ul className="mt-3 flex flex-col divide-y divide-[#e3dabf]">
        {pesanan.items.map((item) => (
          <li key={item.id_listing} className="flex items-center gap-3 py-2.5">
            <FotoListing
              foto={item.foto}
              alt={item.nama_makanan}
              className="h-[56px] w-[56px] shrink-0 rounded-xl border border-[#d8cfb4]"
            />
            <div className="min-w-0 flex-1">
              <p className="truncate font-extrabold text-[#0b8ea8]">{item.nama_makanan}</p>
              <p className="text-xs text-[#58635b]">
                {item.porsi} · {item.jumlah} portions
              </p>
            </div>
            <p className="shrink-0 text-sm font-bold text-[#1a1a1a]">
              {formatRupiah(item.harga_satuan * item.jumlah)}
            </p>
          </li>
        ))}
      </ul>

      <div className="mt-3 flex items-center justify-between gap-3 border-t border-[#d9d1b5] pt-3">
        <p className="text-sm font-extrabold text-[#1a1a1a]">
          Subtotal: {formatRupiah(pesanan.subtotal)}
        </p>

        {sudahDiambil ? (
          <p className="text-xs text-[#58635b]">
            Picked up {formatWaktu(pesanan.waktu_diambil ?? "")}
          </p>
        ) : (
          <button
            type="button"
            disabled={isMenandai}
            onClick={() => onTandaiDiambil(pesanan.id_transaksi)}
            className="rounded-lg bg-[#1a8ca1] px-4 py-2 text-sm font-bold text-white transition hover:bg-[#14798b] disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isMenandai ? "Updating..." : "Mark as Picked Up"}
          </button>
        )}
      </div>
    </div>
  );
}

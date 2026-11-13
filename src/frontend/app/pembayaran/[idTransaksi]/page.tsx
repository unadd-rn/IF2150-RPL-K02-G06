"use client";
import { Suspense, useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { AppLayout } from "@/components/layout";
import {
  ApiError,
  ambilTransaksi,
  type TransaksiPembayaran,
} from "@/lib/api";

const rupiah = (n: number) => `Rp. ${n.toLocaleString("id-ID")}`;
const pesanDari = (e: unknown) => (e instanceof ApiError ? e.message : "An error occurred");
const PESAN_KEDALUWARSA = "The transaction was canceled because the payment deadline passed.";

function PembayaranIsi() {
  const { idTransaksi } = useParams<{ idTransaksi: string }>();
  const router = useRouter();
  const [trx, setTrx] = useState<TransaksiPembayaran | null>(null);
  const [pesan, setPesan] = useState("");
  const [isSimulating, setIsSimulating] = useState(false);

  // Halaman pembayaran hanya sah untuk id transaksi yang valid (dibuat lewat "Buy Now" di keranjang).
  const idValid = Number.isInteger(Number(idTransaksi)) && Number(idTransaksi) >= 1;

  useEffect(() => {
    if (!idValid) return; // id tidak sah → tampilkan pesan tanpa memanggil API
    let dibatalkan = false;
    let timer: ReturnType<typeof setTimeout> | undefined;
    async function muatStatus() {
      try {
        const t = await ambilTransaksi(idTransaksi);
        if (dibatalkan) return;
        setTrx(t);
        setPesan(t.status === "BATAL" ? PESAN_KEDALUWARSA : "");
        if (t.status === "MENUNGGU_BAYAR") timer = setTimeout(muatStatus, 2000);
      } catch (e) {
        if (dibatalkan) return;
        setPesan(pesanDari(e));
        timer = setTimeout(muatStatus, 3000);
      }
    }
    void muatStatus();
    return () => {
      dibatalkan = true;
      if (timer) clearTimeout(timer);
    };
  }, [idTransaksi, idValid]);

  async function handleSimulatePayment() {
    if (!trx?.url_scan) return;
    const token = new URL(trx.url_scan, window.location.origin).pathname.split("/").filter(Boolean).pop();
    if (!token) {
      setPesan("Could not start the payment simulation. Please try again.");
      return;
    }

    setIsSimulating(true);
    setPesan("");
    try {
      const response = await fetch(`/api/pembayaran/scan/${encodeURIComponent(token)}`, { method: "POST" });
      if (!response.ok) throw new Error("Payment simulation failed. Please try again.");
      const updated = await ambilTransaksi(idTransaksi);
      setTrx(updated);
      setPesan(updated.status === "BATAL" ? PESAN_KEDALUWARSA : "");
    } catch {
      setPesan("Payment simulation failed. Please try again.");
    } finally {
      setIsSimulating(false);
    }
  }

  let isi;
  if (!idValid) {
    // Bukan id transaksi (mis. sisa URL lama /pembayaran/checkout) → tidak ada yang bisa dibayar.
    isi = (
      <div className="space-y-4">
        <p className="font-medium text-red-600">Transaction not found</p>
        <button
          type="button"
          onClick={() => router.push("/katalog")}
          className="w-full rounded-md bg-[#f25f4b] px-4 py-4 text-xl font-black text-white shadow-sm"
        >
          Back to catalog
        </button>
      </div>
    );
  } else if (!trx) {
    isi = <p className="text-[#5d625b]">{pesan || "Loading..."}</p>;
  } else if (trx.status === "LUNAS") {
    isi = (
      <div className="space-y-4">
        <div className="rounded-[18px] border border-[#d7d0b4] bg-[#f7f0dc] p-5 text-center shadow-sm">
          <h2 className="text-xl font-bold text-[#1b8ca3]">Payment successful</h2>
          <p className="mt-3 text-sm text-[#5d625b]">Pickup code</p>
          <p className="mt-1 text-3xl font-black tracking-widest">{trx.kode_pengambilan}</p>
        </div>
        <Ringkasan trx={trx} />
        <button
          type="button"
          onClick={() => router.push("/katalog")}
          className="w-full rounded-md bg-[#f25f4b] px-4 py-4 text-xl font-black text-white shadow-sm"
        >
          Back to catalog
        </button>
      </div>
    );
  } else if (trx.status === "BATAL") {
    isi = (
      <div className="space-y-4">
        <p className="font-medium text-red-600">{pesan || "Transaksi ini sudah dibatalkan"}</p>
        <button
          type="button"
          onClick={() => router.push("/katalog")}
          className="w-full rounded-md bg-[#f25f4b] px-4 py-4 text-xl font-black text-white shadow-sm"
        >
          Back to catalog
        </button>
      </div>
    );
  } else {
    isi = (
      <div className="space-y-4">
        <Ringkasan trx={trx} />
        {trx.kode_qris && (
          <div className="rounded-[18px] border border-[#d7d0b4] bg-[#f7f0dc] p-4 text-center shadow-sm">
            <img src={trx.kode_qris} alt="QRIS dummy" className="mx-auto w-56" />
            <p className="mt-3 text-sm text-[#5d625b]">This demo QR code does not open a link or confirm payment when scanned.</p>
          </div>
        )}
        {pesan && <p className="font-medium text-red-600">{pesan}</p>}
        {trx.url_scan && (
          <button
            type="button"
            onClick={handleSimulatePayment}
            disabled={isSimulating}
            className="block w-full rounded-md bg-[#f25f4b] px-4 py-4 text-center text-xl font-black text-white shadow-sm disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isSimulating ? "Processing payment…" : "Simulate Payment"}
          </button>
        )}
      </div>
    );
  }

  return (
    <AppLayout
      role="buyer"
      isAuthenticated
      title={<h1 className="text-2xl font-bold text-[#fff4f2] text-center sm:text-4xl">Payment</h1>}
      showHeader
      headerClassName="bg-[#1bb0c7] px-5 pb-5 pt-8"
      bodyClassName="bg-[#e6e0c8] px-4 py-5"
    >
      {isi}
    </AppLayout>
  );
}

export default function PembayaranPage() {
  return (
    <Suspense fallback={null}>
      <PembayaranIsi />
    </Suspense>
  );
}

function Ringkasan({ trx }: { trx: TransaksiPembayaran }) {
  return (
    <div className="rounded-[18px] border border-[#d7d0b4] bg-[#f7f0dc] p-4 shadow-sm">
      {trx.items.map((i) => (
        <div key={i.id_listing} className="flex items-start justify-between gap-3 py-1">
          <div>
            <p className="font-bold text-[#1b8ca3]">{i.nama_makanan}</p>
            <p className="text-sm text-[#5d625b]">
              {i.jumlah} portions × {rupiah(i.harga_satuan)}
            </p>
          </div>
          <p className="font-bold">{rupiah(i.jumlah * i.harga_satuan)}</p>
        </div>
      ))}
      <div className="mt-3 flex justify-between border-t border-[#d6cebb] pt-3 text-lg font-bold">
        <span>Total</span>
        <span>{rupiah(trx.total_harga)}</span>
      </div>
    </div>
  );
}

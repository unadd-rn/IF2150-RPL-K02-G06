"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { AppLayout } from "@/components/layout";
import KartuPesananPenjual from "@/components/penjual/KartuPesananPenjual";
import { ambilPesananPenjual, tandaiPesananDiambil, type PesananPenjual } from "@/lib/api";

export default function SellerDashboardPage() {
  const router = useRouter();
  const [pesanan, setPesanan] = useState<PesananPenjual[]>([]);
  const [loading, setLoading] = useState(true);
  const [pesanError, setPesanError] = useState<string | null>(null);
  const [idSedangDitandai, setIdSedangDitandai] = useState<number | null>(null);

  const muatPesanan = useCallback(async () => {
    setPesanError(null);
    try {
      const data = await ambilPesananPenjual();
      setPesanan(data);
    } catch (error: unknown) {
      setPesanError(
        error instanceof Error ? error.message : "A system error occurred",
      );
    }
  }, []);

  useEffect(() => {
    let active = true;
    ambilPesananPenjual()
      .then((data) => {
        if (active) setPesanan(data);
      })
      .catch((error: unknown) => {
        if (active) {
          setPesanError(
            error instanceof Error ? error.message : "A system error occurred",
          );
        }
      })
      .finally(() => {
        if (active) setLoading(false);
      });

    return () => {
      active = false;
    };
  }, []);

  const handleTandaiDiambil = async (idTransaksi: number) => {
    setIdSedangDitandai(idTransaksi);
    setPesanError(null);
    try {
      await tandaiPesananDiambil(idTransaksi);
      await muatPesanan();
    } catch (error: unknown) {
      setPesanError(
        error instanceof Error ? error.message : "Could not mark the order as picked up",
      );
    } finally {
      setIdSedangDitandai(null);
    }
  };

  return (
    <AppLayout
      role="seller"
      isAuthenticated
      title={<h1 className="text-2xl font-bold text-[#fff4f2] text-center sm:text-4xl">Seller Dashboard</h1>}
      showHeader
      theme="green"
      headerClassName="px-5 pb-5 pt-8"
      bodyClassName="px-4 py-5 sm:px-6 lg:px-8"
    >
      <div className="mx-auto max-w-3xl">
        <div className="rounded-[18px] bg-[#f7f0dc] p-5 shadow-sm">
          <p className="text-sm uppercase tracking-[0.12em] text-[#60756b]">
            Manage Your Store
          </p>
          <h3 className="mt-2 text-2xl font-black text-[#1a8ca1]">
            Food Listings
          </h3>
          <p className="mt-2 text-sm text-[#60756b]">
            Add, update, and deactivate your surplus food listings.
          </p>
          <button
            type="button"
            onClick={() => router.push("/penjual/listing")}
            className="mt-5 rounded-lg bg-[#1a8ca1] px-4 py-2 text-sm font-bold text-white hover:bg-[#14798b]"
          >
            Manage Listings
          </button>
        </div>

        <div className="mt-6">
          <h2 className="text-xl font-black text-[#264b4d]">Incoming Orders</h2>
          <p className="mt-1 text-sm text-[#60756b]">
            Items paid for by customers and ready for pickup at your store.
          </p>
        </div>

        {pesanError && (
          <div
            role="alert"
            className="mt-4 flex flex-col gap-3 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700 sm:flex-row sm:items-center sm:justify-between"
          >
            <p>{pesanError}</p>
            <button
              type="button"
              onClick={() => void muatPesanan()}
              className="self-start font-semibold underline sm:self-auto"
            >
              Try again
            </button>
          </div>
        )}

        {loading && !pesanError && (
          <p role="status" className="mt-6 text-center text-[#60756b]">
            Loading orders...
          </p>
        )}

        {!loading && !pesanError && pesanan.length === 0 && (
          <section className="mt-4 rounded-[18px] bg-[#f7f0dc] px-6 py-10 text-center shadow-sm">
            <h3 className="text-lg font-bold text-[#264b4d]">
              No paid orders yet
            </h3>
            <p className="mx-auto mt-2 max-w-md text-sm text-[#60756b]">
              Customer orders will appear here after payment is confirmed.
            </p>
          </section>
        )}

        {!loading && !pesanError && pesanan.length > 0 && (
          <div className="mt-4 flex flex-col gap-4">
            {pesanan.map((item) => (
              <KartuPesananPenjual
                key={item.id_transaksi}
                pesanan={item}
                isMenandai={idSedangDitandai === item.id_transaksi}
                onTandaiDiambil={handleTandaiDiambil}
              />
            ))}
          </div>
        )}
      </div>
    </AppLayout>
  );
}

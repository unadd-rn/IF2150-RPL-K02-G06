"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { AppLayout } from "@/components/layout";
import FotoListing from "@/components/katalog/FotoListing";
import NotifikasiGagal from "@/components/NotifikasiGagal";
import { ApiError, checkoutPembayaran } from "@/lib/api";
import { useCart } from "@/lib/cart";

const rupiah = (n: number) => `Rp. ${n.toLocaleString("id-ID")}`;

export default function CartPage() {
  const router = useRouter();
  const { siap, items, totalItem, totalHarga, tambah, kurangi, hapus, kosongkan } = useCart();
  const [pesan, setPesan] = useState("");
  const [perluLogin, setPerluLogin] = useState(false);
  const [memproses, setMemproses] = useState(false);
  const [stokPenuhUntuk, setStokPenuhUntuk] = useState<string | null>(null);

  async function beliSekarang() {
    if (memproses || items.length === 0) return;
    setMemproses(true);
    setPesan("");
    setPerluLogin(false);
    try {
      // Satu transaksi berisi semua item keranjang (UC05).
      const trx = await checkoutPembayaran(
        items.map((i) => ({ id_listing: i.listing.id_listing, jumlah: i.jumlah })),
      );
      kosongkan();
      router.push(`/pembayaran/${trx.id_transaksi}`);
    } catch (e) {
      if (e instanceof ApiError && (e.status === 401 || e.status === 403)) setPerluLogin(true);
      setPesan(e instanceof ApiError ? e.message : "An error occurred");
      setMemproses(false);
    }
  }

  return (
    <AppLayout
      role="buyer"
      isAuthenticated
      title={<h1 className="text-2xl font-bold text-[#fff4f2] text-center sm:text-4xl">My Cart</h1>}
      showHeader
      theme="blue"
      headerClassName="px-5 pb-5 pt-4"
      bodyClassName="bg-[#e6e0c8] px-4 py-5"
    >
      {!siap ? (
        <p className="text-[#5d625b]">Loading cart…</p>
      ) : items.length === 0 ? (
        <div className="rounded-[18px] border border-[#d7d0b4] bg-[#f7f0dc] p-8 text-center shadow-sm">
          <p className="text-xl font-bold text-[#1b8ca3]">Your cart is empty</p>
          <p className="mt-2 text-sm text-[#5d625b]">
            Add surplus food from the catalog by pressing the + button.
          </p>
          <Link
            href="/katalog"
            className="mt-6 inline-block rounded-md bg-[#1bb0c7] px-6 py-3 font-bold text-white shadow-sm transition hover:brightness-110"
          >
            Browse catalog
          </Link>
        </div>
      ) : (
        <>
          <div className="space-y-4 pb-4">
            {items.map(({ listing, jumlah }) => (
              <div
                key={listing.id_listing}
                className="rounded-[18px] border border-[#d7d0b4] bg-[#f7f0dc] p-3 shadow-sm"
              >
                <div className="flex items-center gap-4">
                  <Link href={`/katalog/${listing.id_listing}`} className="shrink-0">
                    <FotoListing
                      foto={listing.foto}
                      alt={listing.nama_makanan}
                      className="h-[76px] w-[92px] rounded-xl"
                    />
                  </Link>

                  <div className="min-w-0 flex-1">
                    <div className="flex items-start justify-between gap-2">
                      <div className="min-w-0">
                        <h3 className="truncate text-base font-bold text-[#1b8ca3]">
                          {listing.nama_makanan}
                        </h3>
                        <p className="truncate text-sm text-[#5d625b]">
                          {listing.porsi
                            ? `${listing.porsi} · ${rupiah(listing.harga)} / portion`
                            : `${rupiah(listing.harga)} / portion`}
                        </p>
                      </div>
                      <button
                        type="button"
                        onClick={() => hapus(listing.id_listing)}
                    aria-label={`Remove ${listing.nama_makanan} from cart`}
                        className="text-lg leading-none text-[#f15d69] transition hover:brightness-110"
                      >
                        ×
                      </button>
                    </div>

                    <div className="mt-3 flex items-center justify-between">
                      <p className="text-base font-bold text-[#1a1a1a]">
                        {rupiah(listing.harga * jumlah)}
                      </p>
                      <div className="flex items-center gap-1 rounded-md bg-[#ff4d57] px-1 py-1 text-white">
                        <button
                          type="button"
                          onClick={() => kurangi(listing.id_listing)}
                          aria-label={`Decrease quantity of ${listing.nama_makanan}`}
                          className="flex h-8 w-8 items-center justify-center text-base font-bold leading-none transition hover:brightness-110"
                        >
                          −
                        </button>
                        <span className="min-w-8 text-center text-sm font-bold">{jumlah}</span>
                        <button
                          type="button"
                          onClick={() => jumlah >= listing.stok ? setStokPenuhUntuk(listing.nama_makanan) : tambah(listing, 1)}
                          aria-label={`Add ${listing.nama_makanan}`}
                          className="flex h-8 w-8 items-center justify-center text-base font-bold leading-none transition hover:brightness-110"
                        >
                          +
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-6 rounded-t-md border-t border-[#d6cebb] bg-[#e6e0c8] px-1 pt-4">
            <div className="grid grid-cols-[auto_1fr] gap-x-4 gap-y-2 text-sm font-medium text-[#1b1b1b]">
              <span>Total</span>
              <span className="text-right">{rupiah(totalHarga)}</span>
              <span>Discount</span>
              <span className="text-right">{rupiah(0)}</span>
              <span className="text-base font-bold">Subtotal</span>
              <span className="text-right text-base font-bold">{rupiah(totalHarga)}</span>
            </div>

            {pesan && (
              <p className="mt-3 text-sm font-medium text-red-600">
                {pesan}{" "}
                {perluLogin && (
                  <Link href="/login" className="underline">
                    Log in first
                  </Link>
                )}
              </p>
            )}

            <button
              type="button"
              disabled={memproses}
              onClick={beliSekarang}
              className="mt-6 w-full rounded-md bg-[#f25f4b] px-4 py-3 text-base font-bold text-white shadow-sm transition hover:brightness-110 disabled:opacity-60"
            >
              {memproses ? "Memproses..." : `Buy Now (${totalItem})`}
            </button>
          </div>
        </>
      )}
      <NotifikasiGagal
        pesan={stokPenuhUntuk ? `The available stock for ${stokPenuhUntuk} has been reached. Reduce the quantity to continue.` : pesan || null}
        onClose={() => { setStokPenuhUntuk(null); setPesan(""); setPerluLogin(false); }}
      />
    </AppLayout>
  );
}

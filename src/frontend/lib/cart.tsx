"use client";

import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useSyncExternalStore,
  type ReactNode,
} from "react";
import type { ListingKatalog } from "./api";

/** Satu baris keranjang: listing makanan + jumlah porsi yang dipilih pembeli. */
export type ItemKeranjang = { listing: ListingKatalog; jumlah: number };

type KeadaanKeranjang = {
  /** false sampai isi keranjang selesai dibaca dari localStorage (mencegah mismatch SSR). */
  siap: boolean;
  items: ItemKeranjang[];
};

type NilaiKeranjang = KeadaanKeranjang & {
  /** Jumlah porsi suatu listing di keranjang; 0 jika belum ada. */
  qtyDari: (idListing: number) => number;
  /** Tambah porsi listing ke keranjang (dibatasi maksimum stok). */
  tambah: (listing: ListingKatalog, jumlah?: number) => void;
  /** Kurangi 1 porsi; saat mencapai 0 item dihapus dari keranjang (tidak pernah negatif). */
  kurangi: (idListing: number) => void;
  hapus: (idListing: number) => void;
  kosongkan: () => void;
  totalItem: number;
  totalHarga: number;
};

const KUNCI_PENYIMPANAN = "savebite.keranjang.v1";

// ---------- Store eksternal (localStorage) yang dibaca lewat useSyncExternalStore ----------

const KEADAAN_AWAL: KeadaanKeranjang = { siap: false, items: [] };

let keadaan: KeadaanKeranjang = KEADAAN_AWAL;
let sudahMuat = false;
const pendengar = new Set<() => void>();

function isListingValid(nilai: unknown): nilai is ListingKatalog {
  return (
    typeof nilai === "object" &&
    nilai !== null &&
    typeof (nilai as ListingKatalog).id_listing === "number" &&
    typeof (nilai as ListingKatalog).nama_makanan === "string" &&
    typeof (nilai as ListingKatalog).harga === "number" &&
    typeof (nilai as ListingKatalog).stok === "number"
  );
}

function bacaTersimpan(): ItemKeranjang[] {
  try {
    const mentah = window.localStorage.getItem(KUNCI_PENYIMPANAN);
    if (!mentah) return [];
    const data: unknown = JSON.parse(mentah);
    if (!Array.isArray(data)) return [];
    const valid: ItemKeranjang[] = [];
    for (const baris of data) {
      if (
        typeof baris === "object" &&
        baris !== null &&
        isListingValid((baris as ItemKeranjang).listing) &&
        typeof (baris as ItemKeranjang).jumlah === "number"
      ) {
        const { listing, jumlah } = baris as ItemKeranjang;
        if (listing.stok < 1) continue;
        // Batasi jumlah agar wajar: 1..stok (data lama yang tidak valid dibuang diam-diam).
        valid.push({ listing, jumlah: Math.max(1, Math.min(Math.trunc(jumlah), listing.stok)) });
      }
    }
    return valid;
  } catch {
    return [];
  }
}

/** Muat isi keranjang dari localStorage sekali, saat pelanggan (komponen) pertama berlangganan. */
function muatSekali() {
  if (sudahMuat) return;
  sudahMuat = true;
  keadaan = { siap: true, items: bacaTersimpan() };
}

function beriTahu() {
  for (const dengar of pendengar) dengar();
}

function subscribe(dengar: () => void) {
  muatSekali(); // dipanggil hanya di klien (efek langganan tidak jalan saat render server)
  pendengar.add(dengar);
  return () => {
    pendengar.delete(dengar);
  };
}

function ambilSnapshot(): KeadaanKeranjang {
  return keadaan;
}

function ambilSnapshotServer(): KeadaanKeranjang {
  return KEADAAN_AWAL;
}

function simpan(items: ItemKeranjang[]) {
  if (!sudahMuat) return; // jangan menimpa penyimpanan sebelum isi lama terbaca
  try {
    window.localStorage.setItem(KUNCI_PENYIMPANAN, JSON.stringify(items));
  } catch {
    // Gagal simpan (mis. storage penuh/private mode) → keranjang tetap jalan di memori.
  }
}

/** Satu-satunya pintu mengubah keadaan: selalu buat objek baru agar React mendeteksi perubahan. */
function ubahKeadaan(items: ItemKeranjang[]) {
  keadaan = { siap: true, items };
  simpan(items);
  beriTahu();
}

// ---------- Operasi keranjang ----------

function tambahItem(items: ItemKeranjang[], listing: ListingKatalog, jumlah: number): ItemKeranjang[] {
  if (listing.stok < 1 || jumlah < 1) return items;
  const indeks = items.findIndex((i) => i.listing.id_listing === listing.id_listing);
  if (indeks === -1) {
    return [...items, { listing, jumlah: Math.min(jumlah, listing.stok) }];
  }
  const sekarang = items[indeks].jumlah;
  const berikut = Math.min(sekarang + jumlah, listing.stok);
  if (berikut === sekarang) return items; // sudah mentok stok
  const salin = [...items];
  salin[indeks] = { ...salin[indeks], listing, jumlah: berikut };
  return salin;
}

function kurangiItem(items: ItemKeranjang[], idListing: number): ItemKeranjang[] {
  return items.flatMap((i) => {
    if (i.listing.id_listing !== idListing) return [i];
    const berikut = i.jumlah - 1;
    // Mencapai 0 → item keluar dari keranjang; tidak pernah negatif.
    return berikut <= 0 ? [] : [{ ...i, jumlah: berikut }];
  });
}

// ---------- Konteks + hook ----------

const CartContext = createContext<NilaiKeranjang | null>(null);

export function CartProvider({ children }: { children: ReactNode }) {
  // Pola React untuk state eksternal (localStorage): render server memakai snapshot awal,
  // lalu React membandingkan ulang setelah langganan sehingga tidak terjadi hydration mismatch.
  const { siap, items } = useSyncExternalStore(subscribe, ambilSnapshot, ambilSnapshotServer);

  const tambah = useCallback(
    (listing: ListingKatalog, jumlah = 1) => ubahKeadaan(tambahItem(keadaan.items, listing, jumlah)),
    [],
  );
  const kurangi = useCallback(
    (idListing: number) => ubahKeadaan(kurangiItem(keadaan.items, idListing)),
    [],
  );
  const hapus = useCallback((idListing: number) => {
    ubahKeadaan(keadaan.items.filter((i) => i.listing.id_listing !== idListing));
  }, []);
  const kosongkan = useCallback(() => ubahKeadaan([]), []);

  const nilai = useMemo<NilaiKeranjang>(
    () => ({
      siap,
      items,
      qtyDari: (idListing) =>
        items.find((i) => i.listing.id_listing === idListing)?.jumlah ?? 0,
      tambah,
      kurangi,
      hapus,
      kosongkan,
      totalItem: items.reduce((total, i) => total + i.jumlah, 0),
      totalHarga: items.reduce((total, i) => total + i.jumlah * i.listing.harga, 0),
    }),
    [siap, items, tambah, kurangi, hapus, kosongkan],
  );

  return <CartContext.Provider value={nilai}>{children}</CartContext.Provider>;
}

export function useCart(): NilaiKeranjang {
  const ctx = useContext(CartContext);
  if (!ctx) throw new Error("useCart harus dipakai di dalam <CartProvider>");
  return ctx;
}

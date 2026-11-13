"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { ambilDaftarKatalog, ApiError, cariKatalog, type ListingKatalog } from "@/lib/api";
import EmptyState from "./EmptyState";
import KartuListing from "./KartuListing";
import PesanKatalog, { perluLogin, PesanPerluLogin } from "./PesanKatalog";
import { adaPencarian, bacaPencarian } from "./pencarian";

type Hasil = { kunci: string; daftar: ListingKatalog[] | null; error: string | null; harusLogin: boolean };

/**
 * tampilkanDaftar (Algo-C11-01) + kirimPencarian (Algo-C11-03).
 * Tanpa parameter di URL → semua listing tersedia (UC02); dengan kata kunci/harga → UC04.
 */
export default function DaftarListing() {
  const searchParams = useSearchParams();
  const kunci = searchParams.toString();
  const [hasil, setHasil] = useState<Hasil | null>(null);

  const pencarian = bacaPencarian(searchParams);
  const mencari = adaPencarian(pencarian);

  useEffect(() => {
    const p = bacaPencarian(new URLSearchParams(kunci));
    if (p.hargaTidakValid) return; // ditangani saat render, tidak perlu ke server
    let aktif = true;
    (adaPencarian(p) ? cariKatalog(p) : ambilDaftarKatalog())
      .then((daftar) => aktif && setHasil({ kunci, daftar, error: null, harusLogin: false }))
      .catch((e) => {
        if (!aktif) return;
        setHasil({
          kunci,
          daftar: null,
          error: e instanceof ApiError ? e.message : "Could not load the catalog",
          harusLogin: perluLogin(e),
        });
      });
    return () => {
      aktif = false;
    };
  }, [kunci]);

  // Hasil milik URL sebelumnya dianggap belum dimuat
  const terkini = hasil?.kunci === kunci ? hasil : null;

  const resetPencarian = { href: "/katalog", label: "Reset search" };

  if (pencarian.hargaTidakValid) {
    return (
      <EmptyState jenis="error" judul="Invalid price range" aksi={resetPencarian}>
        {pencarian.pesanHarga}
      </EmptyState>
    );
  }
  if (terkini?.harusLogin) return <PesanPerluLogin />;
  if (terkini?.error) return <PesanKatalog jenis="error">{terkini.error}</PesanKatalog>;
  if (!terkini?.daftar) return <PesanKatalog>{mencari ? "Searching listings…" : "Loading catalog…"}</PesanKatalog>;

  const daftar = terkini.daftar;
  if (daftar.length === 0) {
    // UC02 Alt 1: tidak ada listing tersedia sama sekali
    if (!mencari) {
      return (
        <EmptyState judul="No surplus food is available yet">
          All listings are out of stock or past their expiration date. Please check again later.
        </EmptyState>
      );
    }
    // UC04 Alt 1 (kata kunci) / Alt 2 (rentang harga): hasil pencarian kosong
    return (
      <EmptyState
        judul={
          pencarian.kataKunci
            ? "No food found for that search"
            : "No food found in that price range"
        }
        aksi={resetPencarian}
      >
        {pencarian.kataKunci
          ? `No available listings match “${pencarian.kataKunci}”. Try another search term or adjust the price range.`
          : "Try widening the price range or clearing the filters."}
      </EmptyState>
    );
  }

  return (
    <ul className="grid grid-cols-1 gap-3 sm:grid-cols-2 sm:gap-4 lg:grid-cols-3">
      {daftar.map((listing) => (
        <li key={listing.id_listing}>
          <KartuListing listing={listing} />
        </li>
      ))}
    </ul>
  );
}

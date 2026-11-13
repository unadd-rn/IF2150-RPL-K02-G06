"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { AppLayout } from "@/components/layout";
import KartuListingPenjual from "@/components/penjual/KartuListingPenjual";
import type { ListingMakananPenjual } from "@/components/penjual/KartuListingPenjual";
import DialogKonfirmasiHapus from "@/components/penjual/DialogKonfirmasiHapus";
import { ambilDaftarListingPenjual, hapusListingPenjual } from "@/lib/api";

export default function ListingPenjualPage() {
  const router = useRouter();
  const [listings, setListings] = useState<ListingMakananPenjual[]>([]);
  const [loading, setLoading] = useState(true);
  const [pesanError, setPesanError] = useState<string | null>(null);
  const [selectedListing, setSelectedListing] = useState<ListingMakananPenjual | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    let active = true;
    ambilDaftarListingPenjual()
      .then((data) => {
        if (active) setListings(data);
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

  const ambilDaftarListing = useCallback(async () => {
    setLoading(true);
    setPesanError(null);
    try {
      const data = await ambilDaftarListingPenjual();
      setListings(data);
    } catch (error: unknown) {
      setPesanError(
        error instanceof Error ? error.message : "A system error occurred",
      );
    } finally {
      setLoading(false);
    }
  }, []);

  const handleKonfirmasiHapus = async () => {
    if (!selectedListing) return;

    setIsDeleting(true);
    setPesanError(null);
    try {
      await hapusListingPenjual(selectedListing.id_listing);
      setSelectedListing(null);
      await ambilDaftarListing();
    } catch (error: unknown) {
      setPesanError(
        error instanceof Error ? error.message : "Could not delete listing",
      );
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <AppLayout
      role="seller"
      isAuthenticated
      title={<h1 className="text-2xl font-bold text-[#fff4f2] text-center sm:text-4xl">Manage Listings</h1>}
      theme="blue"
      headerClassName="px-5 pb-5 pt-8"
      bodyClassName="px-4 py-6 sm:px-6 lg:px-8"
    >
      <div className="mx-auto max-w-7xl">
        <div className="mb-6 flex flex-col gap-4 border-b border-[#b9c9bd] pb-5 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-sm font-semibold text-[#60756b]">
              Manage Your Store
            </p>
            <p className="mt-1 text-sm text-[#60756b]">
              Add, edit, or deactivate food listings.
            </p>
          </div>
          <button
            type="button"
            onClick={() => router.push("/penjual/listing/tambah")}
            className="rounded-xl bg-[#1C8CC9] px-5 py-3 text-sm font-bold text-white shadow-sm transition hover:bg-[#166DA2] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#166DA2]"
          >
            + Add Listing
          </button>
        </div>

        {pesanError && (
          <div
            role="alert"
            className="mb-6 flex flex-col gap-3 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700 sm:flex-row sm:items-center sm:justify-between"
          >
            <p>{pesanError}</p>
            <button
              type="button"
              onClick={() => void ambilDaftarListing()}
              className="self-start font-semibold underline sm:self-auto"
            >
              Try again
            </button>
          </div>
        )}

        {loading && (
          <p role="status" className="py-12 text-center text-[#60756b]">
            Loading food listings...
          </p>
        )}

        {!loading && !pesanError && listings.length === 0 && (
          <section className="rounded-2xl bg-[#f7f0dc] px-6 py-14 text-center shadow-sm">
            <h2 className="text-lg font-bold text-[#264b4d]">
              No food listings yet
            </h2>
            <p className="mx-auto mt-2 max-w-md text-sm text-[#60756b]">
              Start selling surplus food by adding your store's first listing.
            </p>
            <button
              type="button"
              onClick={() => router.push("/penjual/listing/tambah")}
              className="mt-5 rounded-xl bg-[#1C8CC9] px-5 py-3 text-sm font-bold text-white hover:bg-[#166DA2]"
            >
              Add Your First Product
            </button>
          </section>
        )}

        {!loading && !pesanError && listings.length > 0 && (
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {listings.map((item) => (
              <KartuListingPenjual
                key={item.id_listing}
                listing={item}
                onEdit={(id) => router.push(`/penjual/listing/${id}/edit`)}
                onHapus={setSelectedListing}
              />
            ))}
          </div>
        )}
      </div>

      <DialogKonfirmasiHapus
        isOpen={selectedListing !== null}
        namaMakanan={selectedListing?.nama_makanan ?? ""}
        isDeleting={isDeleting}
        onConfirm={handleKonfirmasiHapus}
        onCancel={() => setSelectedListing(null)}
      />
    </AppLayout>
  );
}

"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import KartuListingPenjual, {
    ListingMakananPenjual,
} from "@/components/penjual/KartuListingPenjual";
import DialogKonfirmasiHapus from "@/components/penjual/DialogKonfirmasiHapus";

export default function ListingPenjualPage() {
    const router = useRouter();
    const [listings, setListings] = useState<ListingMakananPenjual[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [pesanError, setPesanError] = useState<string | null>(null);

    // State untuk dialog hapus
    const [selectedListing, setSelectedListing] = useState<ListingMakananPenjual | null>(null);
    const [isDeleting, setIsDeleting] = useState<boolean>(false);

    // Fetch daftar listing penjual
    const ambilDaftarListing = async () => {
        try {
        const res = await fetch("/api/listing/penjual", {
            credentials: "same-origin",
            cache: "no-store",
        });

        if (!res.ok) {
            throw new Error("Gagal mengambil daftar listing makanan.");
        }

        const data = await res.json();
        setListings(data);
        setPesanError(null);
        } catch (err: unknown) {
        const message = err instanceof Error ? err.message : "Terjadi kesalahan sistem";
        setPesanError(message);
        } finally {
        setLoading(false);
        }
    };

    useEffect(() => {
        let aktif = true;
        fetch("/api/listing/penjual", { credentials: "same-origin", cache: "no-store" })
        .then((res) => {
            if (!res.ok) throw new Error("Gagal mengambil daftar listing makanan.");
            return res.json();
        })
        .then((data) => {
            if (!aktif) return;
            setListings(data);
            setPesanError(null);
        })
        .catch((err: unknown) => {
            if (!aktif) return;
            setPesanError(err instanceof Error ? err.message : "Terjadi kesalahan sistem");
        })
        .finally(() => {
            if (aktif) setLoading(false);
        });
        return () => {
            aktif = false;
        };
    }, []);

    // Eksekusi Soft Delete (UC09)
    const handleKonfirmasiHapus = async () => {
        if (!selectedListing) return;

        const idTarget = selectedListing.id_listing;
        setIsDeleting(true);
        try {
        const res = await fetch(`/api/listing/${idTarget}`, {
            method: "DELETE",
            credentials: "same-origin",
        });

        if (!res.ok) {
            throw new Error("Gagal menghapus listing.");
        }

        setSelectedListing(null);
        await ambilDaftarListing();
        } catch (err: unknown) {
        const message = err instanceof Error ? err.message : "Gagal menghapus listing";
        alert(message);
        } finally {
        setIsDeleting(false);
        }
    };

    return (
        <main className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-7xl">
            <div className="flex items-center justify-between border-b border-gray-200 pb-5">
            <div>
                <h1 className="text-2xl font-bold text-gray-900">Kelola Listing Makanan</h1>
                <p className="mt-1 text-sm text-gray-500">
                Daftar menu makanan yang Anda jual di SaveBite.
                </p>
            </div>
            <button
                onClick={() => router.push("/penjual/listing/tambah")}
                className="rounded-md bg-emerald-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-emerald-700"
            >
                + Tambah Listing
            </button>
            </div>

            {/* State Loading */}
            {loading && (
            <div className="py-12 text-center text-gray-500">
                Memuat daftar listing makanan...
            </div>
            )}

            {/* State Error */}
            {pesanError && (
            <div className="mt-6 rounded-md bg-red-50 p-4 text-red-700 text-sm">
                {pesanError}
            </div>
            )}

            {/* State Kosong */}
            {!loading && !pesanError && listings.length === 0 && (
            <div className="py-16 text-center">
                <h3 className="text-lg font-medium text-gray-900">Belum ada listing makanan</h3>
                <p className="mt-1 text-sm text-gray-500">
                Mulai jual makanan penyelamatan Anda dengan menambahkan listing baru.
                </p>
                <button
                onClick={() => router.push("/penjual/listing/tambah")}
                className="mt-4 rounded-md bg-emerald-600 px-4 py-2 text-sm font-medium text-white hover:bg-emerald-700"
                >
                Tambah Makanan Pertama
                </button>
            </div>
            )}

            {/* Grid Listing Makanan */}
            {!loading && !pesanError && listings.length > 0 && (
            <div className="mt-6 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
                {listings.map((item, index) => {
                const keyId = item.id_listing || index;
                return (
                    <KartuListingPenjual
                    key={keyId}
                    listing={item}
                    onEdit={(id) => id != null && router.push(`/penjual/listing/${id}/edit`)}
                    onHapus={(listingItem) => setSelectedListing(listingItem)}
                    />
                );
                })}
            </div>
            )}

            {/* Pop-up Dialog Hapus */}
            <DialogKonfirmasiHapus
            isOpen={!!selectedListing}
            namaMakanan={selectedListing?.nama_makanan || ""}
            isDeleting={isDeleting}
            onConfirm={handleKonfirmasiHapus}
            onCancel={() => setSelectedListing(null)}
            />
        </div>
        </main>
    );
}
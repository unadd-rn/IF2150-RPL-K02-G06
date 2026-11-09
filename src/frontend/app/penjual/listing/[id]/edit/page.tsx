"use client";

import { useEffect, useState, use } from "react";
import { useRouter } from "next/navigation";
import FormListing from "@/components/penjual/FormListing";
import { ambilDetailListingPenjual, ubahListing, DataListingPayload, ListingKatalog } from "@/lib/api";

export default function PageEditListing({ params }: { params: Promise<{ id: string }> }) {
    const resolvedParams = use(params);
    const router = useRouter();

    const [initialData, setInitialData] = useState<DataListingPayload | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        ambilDetailListingPenjual(resolvedParams.id)
        .then((data: ListingKatalog) => {
            setInitialData({
            nama_makanan: data.nama_makanan,
            deskripsi: data.deskripsi,
            porsi: data.porsi,
            kondisi: data.kondisi,
            harga: data.harga,
            stok: data.stok,
            batas_kedaluwarsa: data.batas_kedaluwarsa,
            foto: data.foto,
            });
        })
        .catch((err) => {
            setError(err.message || "Gagal mengambil data listing");
        })
        .finally(() => {
            setLoading(false);
        });
    }, [resolvedParams.id]);

    const handleEdit = async (data: DataListingPayload) => {
        await ubahListing(resolvedParams.id, data);
        router.push("/penjual/listing");
    };

    if (loading) {
        return (
        <div className="flex h-64 items-center justify-center">
            <p className="text-gray-500">Memuat data listing...</p>
        </div>
        );
    }

    if (error || !initialData) {
        return (
        <div className="mx-auto max-w-lg mt-10 rounded-md bg-red-50 p-4 text-center border border-red-200">
            <p className="text-red-700">{error || "Data tidak ditemukan"}</p>
            <button
            onClick={() => router.push("/penjual/listing")}
            className="mt-4 rounded-md bg-gray-800 px-4 py-2 text-sm text-white"
            >
            Kembali ke Daftar Listing
            </button>
        </div>
        );
    }

    return (
        <div className="container mx-auto px-4 py-8">
        <FormListing initialData={initialData} onSubmit={handleEdit} isEditing={true} />
        </div>
    );
}
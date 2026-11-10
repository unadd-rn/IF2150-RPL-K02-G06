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
            deskripsi: data.deskripsi ?? "",
            porsi: data.porsi,
            kondisi: data.kondisi,
            harga: data.harga,
            stok: data.stok,
            batas_kedaluwarsa: data.batas_kedaluwarsa,
            foto: data.foto ?? "",
            draft: data.draft,
            });
        })
        .catch((err) => {
            setError(err.message || "Could not load listing details");
        })
        .finally(() => {
            setLoading(false);
        });
    }, [resolvedParams.id]);

    const handleEdit = async (data: DataListingPayload, draft: boolean) => {
        await ubahListing(resolvedParams.id, { ...data, draft });
        router.push("/penjual/listing");
    };

    if (loading) {
        return (
        <div className="flex h-64 items-center justify-center">
            <p className="text-gray-500">Loading listing details...</p>
        </div>
        );
    }

    if (error || !initialData) {
        return (
        <div className="mx-auto max-w-lg mt-10 rounded-md bg-red-50 p-4 text-center border border-red-200">
            <p className="text-red-700">{error || "Listing not found"}</p>
            <button
            onClick={() => router.push("/penjual/listing")}
            className="mt-4 rounded-md bg-gray-800 px-4 py-2 text-sm text-white"
            >
            Back to Listings
            </button>
        </div>
        );
    }

    return <FormListing initialData={initialData} onSubmit={handleEdit} isEditing />;
}

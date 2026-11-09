"use client";

import { useState, useEffect, ChangeEvent, FormEvent } from "react";
import { useRouter } from "next/navigation";
import { DataListingPayload, uploadFotoListing, urlFoto } from "@/lib/api";
import DialogKonfirmasiKeluar from "./DialogKonfirmasiKeluar";

interface FormListingProps {
    initialData?: DataListingPayload;
    onSubmit: (data: DataListingPayload) => Promise<void>;
    isEditing?: boolean;
    }

    export default function FormListing({ initialData, onSubmit, isEditing = false }: FormListingProps) {
    const router = useRouter();

    const [namaMakanan, setNamaMakanan] = useState(initialData?.nama_makanan ?? "");
    const [deskripsi, setDeskripsi] = useState(initialData?.deskripsi ?? "");
    const [porsi, setPorsi] = useState(initialData?.porsi ?? "1 Porsi");
    const [kondisi, setKondisi] = useState(initialData?.kondisi ?? "Sangat Baik");
    const [harga, setHarga] = useState<number | "">(initialData?.harga ?? "");
    const [stok, setStok] = useState<number | "">(initialData?.stok ?? "");
    const [batasKedaluwarsa, setBatasKedaluwarsa] = useState(
        initialData?.batas_kedaluwarsa ? initialData.batas_kedaluwarsa.slice(0, 16) : ""
    );
    
    const [fotoPath, setFotoPath] = useState<string | null>(initialData?.foto ?? null);
    const [fotoPreview, setFotoPreview] = useState<string | null>(urlFoto(initialData?.foto));
    const [fileFoto, setFileFoto] = useState<File | null>(null);

    const [errors, setErrors] = useState<string[]>([]);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [isDirty, setIsDirty] = useState(false);
    const [showExitModal, setShowExitModal] = useState(false);

    // Mencegah navigasi tab/reload tidak sengaja jika form sudah diubah
    useEffect(() => {
        const handleBeforeUnload = (e: BeforeUnloadEvent) => {
        if (isDirty) {
            e.preventDefault();
            e.returnValue = "";
        }
        };
        window.addEventListener("beforeunload", handleBeforeUnload);
        return () => window.removeEventListener("beforeunload", handleBeforeUnload);
    }, [isDirty]);

    // Validasi Input (Kelas Validasi)
    const validasiListing = (): string[] => {
        const errs: string[] = [];
        if (!namaMakanan.trim()) errs.push("Nama makanan wajib diisi.");
        if (!porsi.trim()) errs.push("Informasi porsi wajib diisi.");
        if (!kondisi.trim()) errs.push("Kondisi makanan wajib diisi.");
        if (harga === "" || Number(harga) < 0) errs.push("Harga harus bernilai non-negatif.");
        if (stok === "" || Number(stok) < 0) errs.push("Stok harus bernilai non-negatif.");
        if (!batasKedaluwarsa) {
        errs.push("Batas kedaluwarsa wajib diisi.");
        } else {
        const selectedDate = new Date(batasKedaluwarsa);
        if (selectedDate <= new Date()) {
            errs.push("Batas kedaluwarsa harus di waktu mendatang.");
        }
        }
        return errs;
    };

    const handleFotoChange = (e: ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;

        // Validasi Ukuran (Maks 10 MB) dan Ekstensi
        if (file.size > 10 * 1024 * 1024) {
        setErrors(["Ukuran foto berkas maksimal 10 MB"]);
        return;
        }
        if (!["image/jpeg", "image/jpg", "image/png"].includes(file.type)) {
        setErrors(["Format foto harus berupa PNG atau JPG"]);
        return;
        }

        setFileFoto(file);
        setFotoPreview(URL.createObjectURL(file));
        setIsDirty(true);
        setErrors([]);
    };

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        const validationErrors = validasiListing();
        if (validationErrors.length > 0) {
        setErrors(validationErrors);
        return;
        }

        setIsSubmitting(true);
        setErrors([]);

        try {
        let finalFotoPath = fotoPath;
        if (fileFoto) {
            finalFotoPath = await uploadFotoListing(fileFoto);
        }

        const payload: DataListingPayload = {
            nama_makanan: namaMakanan,
            deskripsi: deskripsi || null,
            porsi,
            kondisi,
            harga: Number(harga),
            stok: Number(stok),
            batas_kedaluwarsa: new Date(batasKedaluwarsa).toISOString(),
            foto: finalFotoPath,
        };

        await onSubmit(payload);
        setIsDirty(false);
        } catch (err: unknown) {
        const message = err instanceof Error ? err.message : "Terjadi kesalahan saat menyimpan data.";
        setErrors([message]);
        } finally {
        setIsSubmitting(false);
        }
    };

    const handleBatalClick = () => {
        if (isDirty) {
        setShowExitModal(true);
        } else {
        router.push("/penjual/listing");
        }
    };

    return (
        <>
        <form onSubmit={handleSubmit} className="mx-auto max-w-2xl space-y-6 rounded-lg bg-white p-6 shadow-md">
            <h2 className="text-2xl font-bold text-gray-800">
            {isEditing ? "Edit Listing Makanan" : "Tambah Listing Makanan Baru"}
            </h2>

            {/* Pesan Error Validasi */}
            {errors.length > 0 && (
            <div className="rounded-md bg-red-50 p-4 border border-red-200">
                <h4 className="text-sm font-semibold text-red-800">Gagal menyimpan data:</h4>
                <ul className="mt-1 list-disc pl-5 text-sm text-red-700">
                {errors.map((err, idx) => (
                    <li key={idx}>{err}</li>
                ))}
                </ul>
            </div>
            )}

            {/* Nama Makanan */}
            <div>
            <label className="block text-sm font-medium text-gray-700">Nama Makanan *</label>
            <input
                type="text"
                value={namaMakanan}
                onChange={(e) => { setNamaMakanan(e.target.value); setIsDirty(true); }}
                className="mt-1 w-full rounded-md border border-gray-300 p-2 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                placeholder="Contoh: Nasi Goreng Spesial"
                required
            />
            </div>

            {/* Deskripsi */}
            <div>
            <label className="block text-sm font-medium text-gray-700">Deskripsi</label>
            <textarea
                value={deskripsi}
                onChange={(e) => { setDeskripsi(e.target.value); setIsDirty(true); }}
                rows={3}
                className="mt-1 w-full rounded-md border border-gray-300 p-2 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                placeholder="Deskripsi kondisi makanan atau detail porsi..."
            />
            </div>

            {/* Porsi & Kondisi */}
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
                <label className="block text-sm font-medium text-gray-700">Porsi *</label>
                <input
                type="text"
                value={porsi}
                onChange={(e) => { setPorsi(e.target.value); setIsDirty(true); }}
                className="mt-1 w-full rounded-md border border-gray-300 p-2 shadow-sm"
                placeholder="Contoh: 1 Porsi / 500gr"
                required
                />
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-700">Kondisi *</label>
                <select
                value={kondisi}
                onChange={(e) => { setKondisi(e.target.value); setIsDirty(true); }}
                className="mt-1 w-full rounded-md border border-gray-300 p-2 shadow-sm"
                >
                <option value="Sangat Baik">Sangat Baik</option>
                <option value="Baik">Baik</option>
                <option value="Layak Konsumsi">Layak Konsumsi</option>
                </select>
            </div>
            </div>

            {/* Harga & Stok */}
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
                <label className="block text-sm font-medium text-gray-700">Harga (Rp) *</label>
                <input
                type="number"
                min="0"
                value={harga}
                onChange={(e) => { setHarga(e.target.value === "" ? "" : Number(e.target.value)); setIsDirty(true); }}
                className="mt-1 w-full rounded-md border border-gray-300 p-2 shadow-sm"
                required
                />
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-700">Stok *</label>
                <input
                type="number"
                min="0"
                value={stok}
                onChange={(e) => { setStok(e.target.value === "" ? "" : Number(e.target.value)); setIsDirty(true); }}
                className="mt-1 w-full rounded-md border border-gray-300 p-2 shadow-sm"
                required
                />
            </div>
            </div>

            {/* Batas Kedaluwarsa */}
            <div>
            <label className="block text-sm font-medium text-gray-700">Batas Kedaluwarsa *</label>
            <input
                type="datetime-local"
                value={batasKedaluwarsa}
                onChange={(e) => { setBatasKedaluwarsa(e.target.value); setIsDirty(true); }}
                className="mt-1 w-full rounded-md border border-gray-300 p-2 shadow-sm"
                required
            />
            </div>

            {/* Upload Foto */}
            <div>
            <label className="block text-sm font-medium text-gray-700">Foto Listing (PNG/JPG, Maks 10MB)</label>
            <input
                type="file"
                accept="image/png, image/jpeg, image/jpg"
                onChange={handleFotoChange}
                className="mt-1 block w-full text-sm text-gray-500 file:mr-4 file:rounded-md file:border-0 file:bg-indigo-50 file:px-4 file:py-2 file:text-sm file:font-semibold file:text-indigo-700 hover:file:bg-indigo-100"
            />
            {fotoPreview && (
                <div className="mt-3">
                <img src={fotoPreview} alt="Preview Foto" className="h-32 w-32 rounded-lg object-cover border" />
                </div>
            )}
            </div>

            {/* Action Buttons */}
            <div className="flex justify-end gap-3 pt-4 border-t">
            <button
                type="button"
                onClick={handleBatalClick}
                disabled={isSubmitting}
                className="rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
                Batal
            </button>
            <button
                type="submit"
                disabled={isSubmitting}
                className="rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 disabled:opacity-50"
            >
                {isSubmitting ? "Menyimpan..." : isEditing ? "Simpan Perubahan" : "Tambah Listing"}
            </button>
            </div>
        </form>

        {/* Dialog Konfirmasi Keluar (UC01 / UC06 Alternate Scenario) */}
        <DialogKonfirmasiKeluar
            isOpen={showExitModal}
            onConfirm={() => router.push("/penjual/listing")}
            onCancel={() => setShowExitModal(false)}
        />
        </>
    );
}
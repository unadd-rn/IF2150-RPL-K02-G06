"use client";

import { useState, useEffect, ChangeEvent, FormEvent } from "react";
import { useRouter } from "next/navigation";
import { DataListingPayload, uploadFotoListing, urlFoto } from "@/lib/api";
import { AppLayout } from "@/components/layout";
import DialogKonfirmasiKeluar from "./DialogKonfirmasiKeluar";
import NotifikasiGagal from "@/components/NotifikasiGagal";

interface FormListingProps {
    initialData?: DataListingPayload;
    onSubmit: (data: DataListingPayload, draft: boolean) => Promise<void>;
    isEditing?: boolean;
    }

    export default function FormListing({ initialData, onSubmit, isEditing = false }: FormListingProps) {
    const router = useRouter();

    const [namaMakanan, setNamaMakanan] = useState(initialData?.nama_makanan ?? "");
    const [deskripsi, setDeskripsi] = useState(initialData?.deskripsi ?? "");
    const [porsi, setPorsi] = useState(initialData?.porsi ?? "1 serving");
    const [kondisi, setKondisi] = useState(initialData?.kondisi ?? "Sangat Baik");
    const [harga, setHarga] = useState<number | "">(initialData?.harga ?? "");
    const [stok, setStok] = useState<number | "">(initialData?.stok ?? "");
    const [batasKedaluwarsa, setBatasKedaluwarsa] = useState(
        initialData?.batas_kedaluwarsa ? initialData.batas_kedaluwarsa.slice(0, 16) : ""
    );
    
    const fotoPath = initialData?.foto || null;
    const [fotoPreview, setFotoPreview] = useState<string | null>(urlFoto(initialData?.foto));
    const [fileFoto, setFileFoto] = useState<File | null>(null);

    const [errors, setErrors] = useState<string[]>([]);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [isDirty, setIsDirty] = useState(false);
    const [showExitModal, setShowExitModal] = useState(false);
    const [notifikasi, setNotifikasi] = useState<string | null>(null);

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

    useEffect(() => {
        return () => {
            if (fotoPreview?.startsWith("blob:")) URL.revokeObjectURL(fotoPreview);
        };
    }, [fotoPreview]);

    // Validasi Input (Kelas Validasi)
    const validasiListing = (): string[] => {
        const errs: string[] = [];
        if (!namaMakanan.trim()) errs.push("Product name is required.");
        if (!deskripsi.trim()) errs.push("Description is required.");
        if (deskripsi.length > 3000) errs.push("Description must be 3,000 characters or fewer.");
        if (!porsi.trim()) errs.push("Serving information is required.");
        if (!kondisi.trim()) errs.push("Product condition is required.");
        if (harga === "" || Number(harga) < 0 || !Number.isInteger(Number(harga))) errs.push("Price must be a non-negative whole number.");
        if (stok === "" || Number(stok) < 0 || !Number.isInteger(Number(stok))) errs.push("Stock must be a non-negative whole number.");
        if (!fotoPath && !fileFoto) errs.push("A product photo is required.");
        if (!batasKedaluwarsa) {
        errs.push("An expiration date is required.");
        } else {
        const selectedDate = new Date(batasKedaluwarsa);
        if (selectedDate <= new Date()) {
            errs.push("The expiration date must be in the future.");
        }
        }
        return errs;
    };

    const handleFotoChange = (e: ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;

        // Validasi Ukuran (Maks 10 MB) dan Ekstensi
        if (file.size > 10 * 1024 * 1024) {
        setErrors(["The photo file must be 10 MB or smaller."]);
        setNotifikasi("The photo file must be 10 MB or smaller.");
        return;
        }
        if (!["image/jpeg", "image/jpg", "image/png"].includes(file.type)) {
        setErrors(["The photo must be a PNG or JPG file."]);
        setNotifikasi("The photo must be a PNG or JPG file.");
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
        setNotifikasi(validationErrors.join(" "));
        return;
        }

        setIsSubmitting(true);
        setErrors([]);

        try {
        let finalFotoPath = fotoPath;
        if (fileFoto) {
            finalFotoPath = await uploadFotoListing(fileFoto);
        }
        if (!finalFotoPath) {
            throw new Error("A product photo is required.");
        }

        const submitter = (e.nativeEvent as SubmitEvent).submitter as HTMLButtonElement | null;
        const simpanSebagaiDraft = submitter?.value === "draft";
        const payload: DataListingPayload = {
            nama_makanan: namaMakanan.trim(),
            deskripsi: deskripsi.trim(),
            porsi: porsi.trim(),
            kondisi: kondisi.trim(),
            harga: Number(harga),
            stok: Number(stok),
            batas_kedaluwarsa: new Date(batasKedaluwarsa).toISOString(),
            foto: finalFotoPath,
            draft: simpanSebagaiDraft,
        };

        await onSubmit(payload, simpanSebagaiDraft);
        setIsDirty(false);
        } catch (err: unknown) {
        const message = err instanceof Error ? err.message : "An error occurred while saving the product.";
        setErrors([message]);
        setNotifikasi(message);
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

    const isFormValid = validasiListing().length === 0;

    return (
        <AppLayout
            role="seller"
            isAuthenticated
            title={
                    <h1 className="text-2xl font-bold text-[#fff4f2] text-center sm:text-4xl">

                    {isEditing ? "Edit Product" : "Add Product"}
                </h1>
            }
            theme="blue"
            headerClassName="px-5 pb-5 pt-8"
            bodyClassName="px-4 py-6 sm:px-6"
        >
        <form onSubmit={handleSubmit} className="mx-auto max-w-2xl space-y-6 rounded-2xl bg-[#f7f0dc] p-5 shadow-sm sm:p-7">
            <h2 className="text-lg font-bold text-[#264b4d]">Product details</h2>

            {/* Pesan Error Validasi */}
            {errors.length > 0 && (
            <div className="rounded-md bg-red-50 p-4 border border-red-200">
                <h4 className="text-sm font-semibold text-red-800">Could not save product:</h4>
                <ul className="mt-1 list-disc pl-5 text-sm text-red-700">
                {errors.map((err, idx) => (
                    <li key={idx}>{err}</li>
                ))}
                </ul>
            </div>
            )}

            {/* Foto produk berada di bagian atas sesuai UI-06 */}
            <div>
            <p className="block text-sm font-bold text-[#264b4d]">
                Product Photo* <span className="font-normal text-[#60756b]">(PNG/JPG, max. 10 MB)</span>
            </p>
            <label
                htmlFor="foto-listing"
                className="mt-2 flex min-h-28 cursor-pointer flex-col items-center justify-center gap-2 rounded-xl border-2 border-dashed border-[#ef5a61] bg-white/60 px-4 py-5 text-center text-sm font-semibold text-[#d84b54] hover:bg-white"
            >
                <span className="text-2xl leading-none" aria-hidden="true">+</span>
                <span>{fileFoto ? fileFoto.name : "Add Photo"}</span>
                <input
                    id="foto-listing"
                    type="file"
                    accept="image/png, image/jpeg, image/jpg"
                    aria-label="Product Photo"
                    onChange={handleFotoChange}
                    className="sr-only"
                />
            </label>
            {fotoPreview && (
                <div className="mt-3">
                <img src={fotoPreview} alt="Product photo preview" className="h-32 w-32 rounded-xl border border-[#d8cfb4] object-cover" />
                </div>
            )}
            </div>

            {/* Nama Makanan */}
            <div>
            <label htmlFor="nama-makanan" className="block text-sm font-bold text-[#264b4d]">Product Name *</label>
            <input
                id="nama-makanan"
                type="text"
                value={namaMakanan}
                onChange={(e) => { setNamaMakanan(e.target.value); setIsDirty(true); }}
                className="mt-1 w-full rounded-xl border border-[#d8cfb4] bg-white/80 px-4 py-3 text-[#264b4d] shadow-sm focus:border-[#1a8ca1] focus:outline-none focus:ring-2 focus:ring-[#1a8ca1]/20"
                placeholder="Enter product name"
                required
            />
            </div>

            {/* Porsi & Kondisi */}
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
                <label htmlFor="porsi" className="block text-sm font-bold text-[#264b4d]">Serving *</label>
                <input
                id="porsi"
                type="text"
                value={porsi}
                onChange={(e) => { setPorsi(e.target.value); setIsDirty(true); }}
                className="mt-1 w-full rounded-xl border border-[#d8cfb4] bg-white/80 px-4 py-3 text-[#264b4d] shadow-sm focus:border-[#1a8ca1] focus:outline-none focus:ring-2 focus:ring-[#1a8ca1]/20"
                placeholder="Example: 1 serving / 500 g"
                required
                />
            </div>

            <div>
                <label htmlFor="kondisi" className="block text-sm font-bold text-[#264b4d]">Condition *</label>
                <select
                id="kondisi"
                value={kondisi}
                onChange={(e) => { setKondisi(e.target.value); setIsDirty(true); }}
                className="mt-1 w-full rounded-xl border border-[#d8cfb4] bg-white/80 px-4 py-3 text-[#264b4d] shadow-sm focus:border-[#1a8ca1] focus:outline-none focus:ring-2 focus:ring-[#1a8ca1]/20"
                >
                <option value="Sangat Baik">Excellent</option>
                <option value="Baik">Good</option>
                <option value="Layak Konsumsi">Safe to Eat</option>
                </select>
            </div>
            </div>

            {/* Harga & Stok */}
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
                <label htmlFor="harga" className="block text-sm font-bold text-[#264b4d]">Price (Rp) *</label>
                <input
                id="harga"
                type="number"
                min="0"
                value={harga}
                onChange={(e) => { setHarga(e.target.value === "" ? "" : Number(e.target.value)); setIsDirty(true); }}
                onBlur={() => { if (harga !== "" && (Number(harga) < 0 || !Number.isInteger(Number(harga)))) setNotifikasi("Price must be a non-negative whole number."); }}
                className="mt-1 w-full rounded-xl border border-[#d8cfb4] bg-white/80 px-4 py-3 text-[#264b4d] shadow-sm focus:border-[#1a8ca1] focus:outline-none focus:ring-2 focus:ring-[#1a8ca1]/20"
                required
                />
            </div>

            <div>
                <label htmlFor="stok" className="block text-sm font-bold text-[#264b4d]">Stock *</label>
                <input
                id="stok"
                type="number"
                min="0"
                value={stok}
                onChange={(e) => { setStok(e.target.value === "" ? "" : Number(e.target.value)); setIsDirty(true); }}
                onBlur={() => { if (stok !== "" && (Number(stok) < 0 || !Number.isInteger(Number(stok)))) setNotifikasi("Stock must be a non-negative whole number."); }}
                className="mt-1 w-full rounded-xl border border-[#d8cfb4] bg-white/80 px-4 py-3 text-[#264b4d] shadow-sm focus:border-[#1a8ca1] focus:outline-none focus:ring-2 focus:ring-[#1a8ca1]/20"
                required
                />
            </div>
            </div>

            {/* Deskripsi */}
            <div>
            <label htmlFor="deskripsi" className="block text-sm font-bold text-[#264b4d]">
                Description * <span className="font-normal text-[#60756b]">{deskripsi.length}/3000</span>
            </label>
            <textarea
                id="deskripsi"
                value={deskripsi}
                onChange={(e) => { setDeskripsi(e.target.value); setIsDirty(true); }}
                rows={3}
                maxLength={3000}
                className="mt-1 w-full rounded-xl border border-[#d8cfb4] bg-white/80 px-4 py-3 text-[#264b4d] shadow-sm focus:border-[#1a8ca1] focus:outline-none focus:ring-2 focus:ring-[#1a8ca1]/20"
                placeholder="Describe the product"
                required
            />
            </div>

            {/* Batas Kedaluwarsa */}
            <div>
            <label htmlFor="batas-kedaluwarsa" className="block text-sm font-bold text-[#264b4d]">Expiry Date *</label>
            <input
                id="batas-kedaluwarsa"
                type="datetime-local"
                value={batasKedaluwarsa}
                onChange={(e) => { setBatasKedaluwarsa(e.target.value); setIsDirty(true); }}
                onBlur={() => { if (batasKedaluwarsa && new Date(batasKedaluwarsa) <= new Date()) setNotifikasi("The expiration date must be in the future. Update it before saving or publishing the listing."); }}
                className="mt-1 w-full rounded-xl border border-[#d8cfb4] bg-white/80 px-4 py-3 text-[#264b4d] shadow-sm focus:border-[#1a8ca1] focus:outline-none focus:ring-2 focus:ring-[#1a8ca1]/20"
                required
            />
            </div>

            {/* Action Buttons */}
            <div className="flex flex-col gap-3 border-t border-[#d9d1b5] pt-5 sm:flex-row sm:justify-end">
            <button
                type="button"
                onClick={handleBatalClick}
                disabled={isSubmitting}
                className="w-full whitespace-nowrap rounded-xl border border-[#d8cfb4] bg-white px-4 py-2.5 text-sm font-semibold text-[#496864] hover:bg-[#f3efe6] sm:w-auto"
            >
                Cancel
            </button>
            <button
                type="submit"
                name="aksi-listing"
                value="draft"
                disabled={isSubmitting || !isFormValid}
                className="w-full whitespace-nowrap rounded-xl border border-[#1C8CC9] bg-white px-5 py-2.5 text-sm font-bold text-[#1C8CC9] hover:bg-[#e7f3fb] disabled:cursor-not-allowed disabled:opacity-50 sm:w-auto"
            >
                {isSubmitting ? "Saving..." : "Save Draft"}
            </button>
            <button
                type="submit"
                name="aksi-listing"
                value="show"
                disabled={isSubmitting || !isFormValid}
                className="w-full whitespace-nowrap rounded-xl bg-[#1C8CC9] px-5 py-2.5 text-sm font-bold text-white hover:bg-[#166DA2] disabled:cursor-not-allowed disabled:opacity-50 sm:w-auto"
            >
                {isSubmitting ? "Saving..." : isEditing ? "Save Changes / Show" : "Show"}
            </button>
            </div>
        </form>

        <DialogKonfirmasiKeluar
            isOpen={showExitModal}
            onConfirm={() => router.push("/penjual/listing")}
            onCancel={() => setShowExitModal(false)}
        />
        <NotifikasiGagal pesan={notifikasi} onClose={() => setNotifikasi(null)} />
        </AppLayout>
    );
}

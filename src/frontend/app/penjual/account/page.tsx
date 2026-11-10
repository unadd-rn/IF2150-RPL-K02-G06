"use client";

import { useEffect, FormEvent, useState } from "react";
import { AppLayout } from "@/components/layout";
import TombolKeluar from "@/components/akun/TombolKeluar";
import { ambilProfilToko, ubahProfilToko, type ProfilToko } from "@/lib/api";

export default function AkunPenjualPage() {
  const [profil, setProfil] = useState<ProfilToko | null>(null);
  const [loading, setLoading] = useState(true);
  const [pesanError, setPesanError] = useState<string | null>(null);

  // Form profil toko
  const [namaToko, setNamaToko] = useState("");
  const [alamatToko, setAlamatToko] = useState("");
  const [isSaving, setIsSaving] = useState(false);
  const [errors, setErrors] = useState<string[]>([]);
  const [pesanSukses, setPesanSukses] = useState<string | null>(null);

  useEffect(() => {
    let aktif = true;
    ambilProfilToko()
      .then((data) => {
        if (!aktif) return;
        setProfil(data);
        setNamaToko(data.nama_toko);
        setAlamatToko(data.alamat_toko);
      })
      .catch((error: unknown) => {
        if (aktif) {
          setPesanError(
            error instanceof Error ? error.message : "A system error occurred",
          );
        }
      })
      .finally(() => {
        if (aktif) setLoading(false);
      });
    return () => {
      aktif = false;
    };
  }, []);

  const validasiForm = (): string[] => {
    const errs: string[] = [];
    if (!namaToko.trim()) errs.push("Store name is required.");
    else if (namaToko.trim().length > 100) errs.push("Store name must be 100 characters or fewer.");
    if (!alamatToko.trim()) errs.push("Store address is required.");
    else if (alamatToko.trim().length > 200) errs.push("Store address must be 200 characters or fewer.");
    return errs;
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    const validationErrors = validasiForm();
    if (validationErrors.length > 0) {
      setErrors(validationErrors);
      setPesanSukses(null);
      return;
    }

    setIsSaving(true);
    setErrors([]);
    setPesanSukses(null);
    try {
      await ubahProfilToko({
        nama_toko: namaToko.trim(),
        alamat_toko: alamatToko.trim(),
      });
      setProfil((data) => (data
        ? { ...data, nama_toko: namaToko.trim(), alamat_toko: alamatToko.trim() }
        : data));
      setPesanSukses("Profil toko berhasil diperbarui");
    } catch (error: unknown) {
      setErrors([
        error instanceof Error ? error.message : "Could not update store profile",
      ]);
    } finally {
      setIsSaving(false);
    }
  };

  const labelKelas = "block text-sm font-bold text-[#264b4d]";
  const inputKelas =
    "mt-1 w-full rounded-xl border border-[#d8cfb4] bg-white/80 px-4 py-3 text-[#264b4d] shadow-sm focus:border-[#1a8ca1] focus:outline-none focus:ring-2 focus:ring-[#1a8ca1]/20";

  return (
    <AppLayout
      role="seller"
      isAuthenticated
      title={<h1 className="text-2xl font-bold text-[#fff4f2] text-center sm:text-4xl">Seller Account</h1>}
      showHeader
      theme="pink"
      headerClassName="px-5 pb-5 pt-8"
      bodyClassName="px-4 py-5 sm:px-6 lg:px-8"
    >
      <div className="mx-auto max-w-2xl">
        {pesanError && (
          <div
            role="alert"
            className="mb-6 flex flex-col gap-3 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700 sm:flex-row sm:items-center sm:justify-between"
          >
            <p>{pesanError}</p>
            <button
              type="button"
              onClick={() => window.location.reload()}
              className="self-start font-semibold underline sm:self-auto"
            >
              Try again
            </button>
          </div>
        )}

        {loading && !pesanError && (
          <p role="status" className="py-12 text-center text-[#60756b]">
            Loading store profile...
          </p>
        )}

        {!loading && profil && (
          <>
            {/* Info akun (read-only) */}
            <div className="mb-6 rounded-[18px] bg-[#f7f0dc] p-5 shadow-sm">
              <h2 className="text-lg font-bold text-[#264b4d]">Account Information</h2>
              <dl className="mt-3 grid grid-cols-[auto_1fr] gap-x-6 gap-y-2 text-sm">
                <dt className="text-[#60756b]">Name</dt>
                <dd className="font-semibold text-[#1a1a1a]">{profil.nama_akun}</dd>
                <dt className="text-[#60756b]">Store</dt>
                <dd className="font-semibold text-[#1a1a1a]">{profil.nama_toko}</dd>
              </dl>
            </div>

            {/* Ubah profil toko */}
            <form
              onSubmit={handleSubmit}
              className="space-y-5 rounded-[18px] bg-[#f7f0dc] p-5 shadow-sm"
            >
              <div>
                <h2 className="text-lg font-bold text-[#264b4d]">Store Profile</h2>
                <p className="mt-1 text-sm text-[#60756b]">
                  This store name and address appear in the customer catalog and
                  and is used as the food pickup location.
                </p>
              </div>

              {errors.length > 0 && (
                <div className="rounded-md border border-red-200 bg-red-50 p-4" role="alert">
                  <ul className="list-disc space-y-1 pl-5 text-sm text-red-700">
                    {errors.map((err, idx) => (
                      <li key={idx}>{err}</li>
                    ))}
                  </ul>
                </div>
              )}

              {pesanSukses && (
                <p
                  className="rounded-md border border-green-200 bg-green-50 p-3 text-sm font-semibold text-green-700"
                  role="status"
                >
                  {pesanSukses}
                </p>
              )}

              <div>
                <label htmlFor="nama-toko" className={labelKelas}>
                  Store Name *
                </label>
                <input
                  id="nama-toko"
                  type="text"
                  value={namaToko}
                  onChange={(e) => setNamaToko(e.target.value)}
                  maxLength={100}
                  className={inputKelas}
                  placeholder="Contoh: Warung Makan Bu Sari"
                  required
                />
              </div>

              <div>
                <label htmlFor="alamat-toko" className={labelKelas}>
                  Store Address (Pickup Location) *
                </label>
                <textarea
                  id="alamat-toko"
                  value={alamatToko}
                  onChange={(e) => setAlamatToko(e.target.value)}
                  rows={3}
                  maxLength={200}
                  className={inputKelas}
                  placeholder="Contoh: Jl. Cikutra No. 88, Bandung"
                  required
                />
              </div>

              <div className="flex justify-end border-t border-[#d9d1b5] pt-4">
                <button
                  type="submit"
                  disabled={isSaving}
                  className="rounded-xl bg-[#1a8ca1] px-5 py-3 text-sm font-bold text-white hover:bg-[#14798b] disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {isSaving ? "Saving..." : "Save Changes"}
                </button>
              </div>
            </form>

            <div className="mt-6 rounded-[18px] bg-[#f7f0dc] p-5 shadow-sm">
              <h2 className="text-lg font-bold text-[#264b4d]">Log Out</h2>
              <p className="mt-1 text-sm text-[#60756b]">
                Your session will end and you will return to the log in page.
              </p>
              <div className="mt-4">
                <TombolKeluar />
              </div>
            </div>
          </>
        )}
      </div>
    </AppLayout>
  );
}

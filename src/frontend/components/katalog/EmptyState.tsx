import Link from "next/link";
import type { ReactNode } from "react";

type Aksi = { href: string; label: string };

type Props = {
  judul: string;
  children?: ReactNode;
  /** Tombol tindak lanjut, mis. reset pencarian atau kembali ke katalog */
  aksi?: Aksi;
  jenis?: "info" | "error";
};

/**
 * tampilkanPesan untuk skenario alternatif katalog: katalog kosong (UC02), listing sudah
 * tidak tersedia (UC03), hasil cari/filter tidak ditemukan & rentang harga tidak valid (UC04).
 */
export default function EmptyState({ judul, children, aksi, jenis = "info" }: Props) {
  const warna =
    jenis === "error"
      ? "border-red-200 bg-red-50 dark:border-red-900 dark:bg-red-950"
      : "border-zinc-200 bg-zinc-50 dark:border-zinc-800 dark:bg-zinc-900";
  const warnaJudul = jenis === "error" ? "text-red-700 dark:text-red-300" : "text-zinc-800 dark:text-zinc-200";

  return (
    <section
      role={jenis === "error" ? "alert" : "status"}
      className={`flex flex-col items-center gap-3 rounded-xl border border-dashed px-6 py-12 text-center ${warna}`}
    >
      <h2 className={`text-lg font-semibold ${warnaJudul}`}>{judul}</h2>
      {children && <p className="max-w-md text-sm text-zinc-600 dark:text-zinc-400">{children}</p>}
      {aksi && (
        <Link
          href={aksi.href}
          className="mt-2 rounded-lg bg-emerald-600 px-4 py-2 text-sm font-semibold text-white hover:bg-emerald-700"
        >
          {aksi.label}
        </Link>
      )}
    </section>
  );
}

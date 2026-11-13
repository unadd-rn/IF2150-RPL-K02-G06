export function formatRupiah(nilai: number): string {
  return new Intl.NumberFormat("id-ID", { style: "currency", currency: "IDR", maximumFractionDigits: 0 }).format(nilai);
}

/** "2026-11-04 18:00:00" / "2026-11-04T18:00:00" → "4 Nov 2026, 18.00" (waktu lokal) */
export function formatWaktu(nilai: string): string {
  const d = new Date(nilai.replace(" ", "T"));
  if (Number.isNaN(d.getTime())) return nilai;
  return new Intl.DateTimeFormat("en-ID", { dateStyle: "medium", timeStyle: "short" }).format(d);
}

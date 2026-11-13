// Nama query param di URL /katalog sama dengan query param backend GET /api/katalog.
export const PARAM_KATA_KUNCI = "kata_kunci";
export const PARAM_HARGA_MIN = "harga_min";
export const PARAM_HARGA_MAKS = "harga_maks";

export type Pencarian = {
  kataKunci: string | null;
  hargaMin: number | null;
  hargaMaks: number | null;
  /** true jika harga di URL bukan bilangan bulat, negatif, atau harga min > harga maks */
  hargaTidakValid: boolean;
  /** Alasan rentang harga tidak valid untuk ditampilkan ke pembeli; null jika valid */
  pesanHarga: string | null;
};

type BacaParam = { get(nama: string): string | null };

function bacaHarga(nilai: string | null): number | null | undefined {
  const s = nilai?.trim();
  if (!s) return null;
  return /^-?\d+$/.test(s) ? Number(s) : undefined;
}

// Aturan sama dengan cariListing (Algo-C16-03) di backend, dicek dulu di klien agar tidak perlu ke server
function validasiHarga(hargaMin: number | null | undefined, hargaMaks: number | null | undefined): string | null {
  if (hargaMin === undefined || hargaMaks === undefined) return "Price must be a whole number";
  if ((hargaMin ?? 0) < 0 || (hargaMaks ?? 0) < 0) return "Price cannot be negative";
  if (hargaMin !== null && hargaMaks !== null && hargaMin > hargaMaks)
    return "Minimum price cannot be greater than maximum price";
  return null;
}

/** Baca kata kunci & rentang harga dari URL. Field kosong berarti filter tidak dipakai. */
export function bacaPencarian(params: BacaParam): Pencarian {
  const hargaMin = bacaHarga(params.get(PARAM_HARGA_MIN));
  const hargaMaks = bacaHarga(params.get(PARAM_HARGA_MAKS));
  const pesanHarga = validasiHarga(hargaMin, hargaMaks);
  return {
    kataKunci: params.get(PARAM_KATA_KUNCI)?.trim() || null,
    hargaMin: hargaMin ?? null,
    hargaMaks: hargaMaks ?? null,
    hargaTidakValid: pesanHarga !== null,
    pesanHarga,
  };
}

export function adaPencarian(p: Pencarian): boolean {
  return p.kataKunci !== null || p.hargaMin !== null || p.hargaMaks !== null || p.hargaTidakValid;
}

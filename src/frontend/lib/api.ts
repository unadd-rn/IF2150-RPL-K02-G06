// API client bersama. Tiap fitur hanya menambah fungsi miliknya sendiri.

export const API_URL = (process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000").replace(/\/+$/, "");

/** URL foto listing sesuai kontrak P2 ↔ P3: NEXT_PUBLIC_API_URL + "/" + foto. null jika tidak ada foto. */
export function urlFoto(foto: string | null | undefined): string | null {
  return foto ? `${API_URL}/${foto.replace(/^\/+/, "")}` : null;
}

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

// Request ke "/api/..." diteruskan ke backend lewat rewrites di next.config.ts (same-origin),
// jadi cookie sesi httpOnly "session_token" dari login P1 ikut terkirim otomatis.
async function getJson<T>(path: string): Promise<T> {
  let res: Response;
  try {
    res = await fetch(path, { credentials: "same-origin", cache: "no-store" });
  } catch {
    throw new ApiError(0, "Tidak dapat terhubung ke server");
  }
  if (!res.ok) {
    let pesan = `Terjadi kesalahan pada server (HTTP ${res.status})`;
    try {
      const body = await res.json();
      if (typeof body?.detail === "string") pesan = body.detail;
    } catch {}
    throw new ApiError(res.status, pesan);
  }
  return res.json() as Promise<T>;
}

// ---------- Katalog (P3: UC02, UC03) ----------

export type ListingKatalog = {
  id_listing: number;
  id_penjual: number;
  nama_makanan: string;
  deskripsi: string | null;
  porsi: string;
  kondisi: string;
  foto: string | null;
  harga: number;
  stok: number;
  batas_kedaluwarsa: string;
};

export function ambilDaftarKatalog(): Promise<ListingKatalog[]> {
  return getJson<ListingKatalog[]>("/api/katalog");
}

export function ambilDetailKatalog(idListing: number | string): Promise<ListingKatalog> {
  return getJson<ListingKatalog>(`/api/katalog/${encodeURIComponent(String(idListing))}`);
}

export type DataListingPayload = {
  nama_makanan: string;
  deskripsi?: string | null;
  porsi: string;
  kondisi: string;
  harga: number;
  stok: number;
  batas_kedaluwarsa: string;
  foto?: string | null;
};

// Mengambil detail listing milik penjual
export function ambilDetailListingPenjual(idListing: number | string): Promise<ListingKatalog> {
  return getJson<ListingKatalog>(`/api/listing/${encodeURIComponent(String(idListing))}`);
}

// Upload Foto Listing (Maks 10MB, JPG/PNG)
export async function uploadFotoListing(file: File): Promise<string> {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch("/api/listing/upload-foto", {
    method: "POST",
    body: formData,
    credentials: "same-origin",
  });

  if (!res.ok) {
    let pesan = "Gagal mengunggah foto makanan";
    try {
      const body = await res.json();
      if (typeof body?.detail === "string") pesan = body.detail;
    } catch {}
    throw new ApiError(res.status, pesan);
  }

  const data = await res.json();
  return data.foto; // Mengembalikan path berkas (misal: /uploads/foto.jpg)
}

// Tambah Listing Baru (UC01)
export async function tambahListing(data: DataListingPayload): Promise<ListingKatalog> {
  const res = await fetch("/api/listing/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
    credentials: "same-origin",
  });

  if (!res.ok) {
    let pesan = "Gagal menambah listing makanan";
    try {
      const body = await res.json();
      if (typeof body?.detail === "string") pesan = body.detail;
    } catch {}
    throw new ApiError(res.status, pesan);
  }

  return res.json();
}

// Ubah Listing (UC06)
export async function ubahListing(idListing: number | string, data: DataListingPayload): Promise<ListingKatalog> {
  const res = await fetch(`/api/listing/${encodeURIComponent(String(idListing))}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
    credentials: "same-origin",
  });

  if (!res.ok) {
    let pesan = "Gagal memperbarui listing makanan";
    try {
      const body = await res.json();
      if (typeof body?.detail === "string") pesan = body.detail;
    } catch {}
    throw new ApiError(res.status, pesan);
  }

  return res.json();
}

// ---------- Cari & filter katalog (P3: UC04) ----------

export type ParamPencarian = {
  kataKunci?: string | null;
  hargaMin?: number | null;
  hargaMaks?: number | null;
};

/** GET /api/katalog?kata_kunci=&harga_min=&harga_maks= — parameter kosong tidak dikirim. */
export function cariKatalog({ kataKunci, hargaMin, hargaMaks }: ParamPencarian): Promise<ListingKatalog[]> {
  const q = new URLSearchParams();
  if (kataKunci?.trim()) q.set("kata_kunci", kataKunci.trim());
  if (hargaMin != null) q.set("harga_min", String(hargaMin));
  if (hargaMaks != null) q.set("harga_maks", String(hargaMaks));
  const qs = q.toString();
  return getJson<ListingKatalog[]>(qs ? `/api/katalog?${qs}` : "/api/katalog");
}

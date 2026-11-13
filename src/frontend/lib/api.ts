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
    throw new ApiError(0, "Could not connect to the server");
  }
  if (!res.ok) {
    const pesan = `A server error occurred (HTTP ${res.status})`;
    throw new ApiError(res.status, pesan);
  }
  return res.json() as Promise<T>;
}

// ---------- Katalog (P3: UC02, UC03) ----------

export type ListingKatalog = {
  id_listing: number;
  id_penjual: number;
  nama_toko: string;
  alamat_toko: string;
  nama_makanan: string;
  deskripsi: string | null;
  porsi: string;
  kondisi: string;
  foto: string | null;
  harga: number;
  stok: number;
  batas_kedaluwarsa: string;
  draft?: boolean;
};

// Listing milik penjual (endpoint /api/listing/penjual) tidak memuat nama/alamat toko
export type ListingPenjual = Omit<ListingKatalog, "nama_toko" | "alamat_toko"> & {
  aktif: boolean;
  draft: boolean;
  tersedia: boolean;
};

export function ambilDaftarListingPenjual(): Promise<ListingPenjual[]> {
  return getJson<ListingPenjual[]>("/api/listing/penjual");
}

export function ambilDaftarKatalog(): Promise<ListingKatalog[]> {
  return getJson<ListingKatalog[]>("/api/katalog");
}

export function ambilDetailKatalog(idListing: number | string): Promise<ListingKatalog> {
  return getJson<ListingKatalog>(`/api/katalog/${encodeURIComponent(String(idListing))}`);
}

export type DataListingPayload = {
  nama_makanan: string;
  deskripsi: string;
  porsi: string;
  kondisi: string;
  harga: number;
  stok: number;
  batas_kedaluwarsa: string;
  foto: string;
  draft?: boolean;
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
    const pesan = "Could not upload the product photo";
    throw new ApiError(res.status, pesan);
  }

  const data = await res.json();
  return data.foto; // Mengembalikan path berkas (misal: /uploads/foto.jpg)
}

// Tambah Listing Baru (UC01)
export async function tambahListing(data: DataListingPayload): Promise<ListingKatalog> {
  const res = await fetch("/api/listing", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
    credentials: "same-origin",
  });

  if (!res.ok) {
    const pesan = "Could not add the food listing";
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
    const pesan = "Could not update the food listing";
    throw new ApiError(res.status, pesan);
  }

  return res.json();
}

export async function hapusListingPenjual(idListing: number | string): Promise<void> {
  const res = await fetch(`/api/listing/${encodeURIComponent(String(idListing))}`, {
    method: "DELETE",
    credentials: "same-origin",
  });

  if (!res.ok) {
    const pesan = "Could not delete the listing";
    throw new ApiError(res.status, pesan);
  }
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

// ---------- Pembayaran (P4: UC05) ----------

export type ItemPembayaran = {
  id_listing: number;
  nama_makanan: string;
  jumlah: number;
  harga_satuan: number;
};

export type TransaksiPembayaran = {
  id_transaksi: number;
  status: "MENUNGGU_BAYAR" | "LUNAS" | "BATAL";
  total_harga: number;
  batas_waktu_bayar: string;
  kode_pengambilan: string | null;
  kode_qris: string | null;
  url_scan: string | null;
  items: ItemPembayaran[];
};

async function postJson<T>(path: string, body?: unknown): Promise<T> {
  let res: Response;
  try {
    res = await fetch(path, {
      method: "POST",
      headers: body !== undefined ? { "Content-Type": "application/json" } : undefined,
      body: body !== undefined ? JSON.stringify(body) : undefined,
      credentials: "same-origin",
    });
  } catch {
    throw new ApiError(0, "Could not connect to the server");
  }
  if (!res.ok) {
    const pesan = `A server error occurred (HTTP ${res.status})`;
    throw new ApiError(res.status, pesan);
  }
  return res.json() as Promise<T>;
}

export type ItemCheckout = { id_listing: number; jumlah: number };

// Checkout seluruh isi keranjang → satu transaksi berisi semua item (UC05).
// kodeKupon (opsional): kode kupon reward pembeli yang ditebus pada subtotal.
export function checkoutPembayaran(items: ItemCheckout[], kodeKupon?: string): Promise<TransaksiPembayaran> {
  const kode = kodeKupon?.trim();
  return postJson<TransaksiPembayaran>("/api/pembayaran/checkout", {
    items,
    ...(kode ? { kode_kupon: kode } : {}),
  });
}

export function ambilTransaksi(id: number | string): Promise<TransaksiPembayaran> {
  return getJson<TransaksiPembayaran>(`/api/pembayaran/${encodeURIComponent(String(id))}`);
}

export function bayarTransaksi(id: number | string): Promise<TransaksiPembayaran> {
  return postJson<TransaksiPembayaran>(`/api/pembayaran/${encodeURIComponent(String(id))}/bayar`);
}

// ---------- Profil toko penjual (P2) ----------

export type ProfilToko = {
  nama_akun: string;
  nama_toko: string;
  alamat_toko: string;
};

// Profil toko milik penjual yang sedang login
export function ambilProfilToko(): Promise<ProfilToko> {
  return getJson<ProfilToko>("/api/toko");
}

export async function ubahProfilToko(data: {
  nama_toko: string;
  alamat_toko: string;
}): Promise<ProfilToko> {
  const res = await fetch("/api/toko", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
    credentials: "same-origin",
  });

  if (!res.ok) {
    const pesan = "Could not update the store profile";
    throw new ApiError(res.status, pesan);
  }

  return res.json();
}

// ---------- Penjualan penjual (pesanan terbayar & pengambilan) ----------

export type ItemPesananPenjual = {
  id_listing: number;
  nama_makanan: string;
  porsi: string;
  foto: string | null;
  jumlah: number;
  harga_satuan: number;
};

export type PesananPenjual = {
  id_transaksi: number;
  tanggal: string;
  total_harga: number;
  subtotal: number;
  kode_pengambilan: string | null;
  waktu_diambil: string | null;
  items: ItemPesananPenjual[];
};

// Pesanan milik toko ini yang SUDAH DIBAYAR pembeli (status LUNAS).
// Menunggu bayar / batal tidak dikirim backend.
export function ambilPesananPenjual(): Promise<PesananPenjual[]> {
  return getJson<PesananPenjual[]>("/api/penjualan/pesanan");
}

// Tandai pesanan "Sudah diambil / Selesai" saat pembeli mengambil di toko.
export async function tandaiPesananDiambil(idTransaksi: number | string): Promise<void> {
  const res = await fetch(
    `/api/penjualan/${encodeURIComponent(String(idTransaksi))}/ambil`,
    { method: "POST", credentials: "same-origin" },
  );

  if (!res.ok) {
    const pesan = "Could not mark the order as picked up";
    throw new ApiError(res.status, pesan);
  }
}

// ---------- Sesi akun (P1) ----------

// Keluar: hapus sesi httpOnly di backend; cookie session_token & role dihapus otomatis oleh respons.
export async function logoutSesi(): Promise<void> {
  await postJson<{ message: string }>("/api/auth/logout");
}

// ---------- Reward (P5: UC08) ----------

export type KuponReward = {
  kode_kupon: string;
  nilai_potongan: number;   // rupiah
  berlaku_sampai: string;   // YYYY-MM-DD
  terpakai: boolean;
  berlaku: boolean;
};

export type ProgresReward = {
  poin_terkumpul: number;
  poin_per_klaim: number;
  poin_per_login: number;
  bisa_klaim: boolean;
  tanggal_login_terakhir: string | null;
  nilai_potongan: number;
  kupon: KuponReward[];
};

export function ambilProgresReward(): Promise<ProgresReward> {
  return getJson<ProgresReward>("/api/reward");
}

export function klaimReward(): Promise<KuponReward> {
  return postJson<KuponReward>("/api/reward/klaim");
}

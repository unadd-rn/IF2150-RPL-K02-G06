import { expect, test } from "@playwright/test";

/**
 * UC05 alur pembeli lewat UI nyata: katalog → keranjang → checkout → pembayaran.
 * Membutuhkan backend FastAPI di localhost:8000 berisi data seed
 * (jalankan `python seed.py` + `uvicorn backend.main:app`).
 */

async function loginSebagaiPembeli(page: import("@playwright/test").Page) {
  await page.goto("/login");
  await page.getByLabel("Email").fill("pembeli@test.com");
  await page.getByRole("textbox", { name: "Password" }).fill("password123");
  await page.getByRole("button", { name: "Log In" }).click();
  await expect(page).toHaveURL(/\/katalog$/);
}

test("pembeli: dari katalog, isi keranjang, checkout, dan bayar lewat UI", async ({ page }) => {
  await loginSebagaiPembeli(page);

  // Pilih listing dengan stok terbanyak (aman dijalankan berulang pada DB seed yang sama).
  // Butuh 3 porsi di bawah, jadi stok minimal 3.
  const nama = await page.evaluate(async () => {
    const daftar: Array<{ id_listing: number; nama_makanan: string; stok: number }> =
      await (await fetch("/api/katalog")).json();
    const pilih = daftar.reduce((a, b) => (b.stok > a.stok ? b : a));
    if (!pilih || pilih.stok < 3) throw new Error("Katalog seed tidak siap (stok < 3)");
    return pilih.nama_makanan;
  });

  // Tambah item dari kartu katalog ke keranjang
  const kartu = page.locator("article", { hasText: nama });
  await expect(kartu.first()).toBeVisible();
  for (let i = 0; i < 2; i++) {
    await kartu.first().getByRole("button", { name: `Add ${nama} to cart` }).click();
  }

  // Tambah satu porsi lagi dari halaman detail listing
  await kartu.first().getByRole("link", { name: `View details for ${nama}` }).click();
  await page.getByRole("button", { name: `Add ${nama} to cart` }).click();

  // Keranjang: item tampil dengan jumlah 3, lalu checkout
  await page.goto("/cart");
  await expect(page.getByRole("heading", { name: "My Cart" })).toBeVisible();
  await expect(page.getByText(nama)).toBeVisible();
  await page.getByRole("button", { name: "Buy Now (3)" }).click();

  // Halaman pembayaran: transaksi dibuat dalam keadaan MENUNGGU_BAYAR dengan QR
  await expect(page).toHaveURL(/\/pembayaran\/\d+$/);
  await expect(page.getByRole("img", { name: "QRIS dummy" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Simulate Payment" })).toBeVisible();

  // Bayar (pembayaran hanya sah lewat tombol Simulate Payment)
  await page.getByRole("button", { name: "Simulate Payment" }).click();
  await expect(page.getByRole("heading", { name: "Payment successful" })).toBeVisible();
  await expect(page.getByText("Pickup code")).toBeVisible();

  // Setelah terbayar, keranjang kembali kosong
  await page.goto("/cart");
  await expect(page.getByText("Your cart is empty")).toBeVisible();
});

test("pembeli: checkout tanpa login ditolak dengan tawaran login", async ({ page }) => {
  // Isi keranjang langsung lewat localStorage tanpa login sama sekali;
  // bentuk listing cukup valid, server tetap menolak karena belum ada sesi.
  await page.addInitScript(() => {
    const listing = {
      id_listing: 1,
      nama_makanan: "Roti Tawar Penyelamatan",
      deskripsi: "roti",
      porsi: "1 Pack",
      kondisi: "Sangat Baik",
      foto: null,
      harga: 12000,
      stok: 5,
      batas_kedaluwarsa: "2999-12-31T23:59:59",
      nama_toko: "Toko Roti Berkah",
      alamat_toko: "Jl. Sudirman No. 45",
    };
    localStorage.setItem("savebite.keranjang.v1", JSON.stringify([{ listing, jumlah: 1 }]));
  });
  await page.goto("/cart");
  await expect(page.getByText("Roti Tawar Penyelamatan")).toBeVisible();

  await page.getByRole("button", { name: "Buy Now (1)" }).click();
  await expect(page.getByRole("link", { name: "Log in first" })).toBeVisible();
  await expect(page).not.toHaveURL(/\/pembayaran\/\d+$/);
});

test("pembeli: kupon reward dari login dipakai di checkout", async ({ page }) => {
  await loginSebagaiPembeli(page);

  // Pilih listing dari katalog (stok >= 2 agar pembeli besar lain tidak menghabiskannya)
  const listing = await page.evaluate(async () => {
    const daftar: Array<{ id_listing: number; nama_makanan: string; stok: number; harga: number }> =
      await (await fetch("/api/katalog")).json();
    const pilih = daftar.reduce((a, b) => (b.stok > a.stok ? b : a));
    if (!pilih || pilih.stok < 2) throw new Error("Katalog seed tidak siap (stok habis)");
    return { nama: pilih.nama_makanan, harga: pilih.harga };
  });

  // Ambil kupon yang masih bisa dipakai: yang sudah diklaim dulu bila ada,
  // kalau tidak maka klaim kupon baru dari poin reward login.
  const kode = await page.evaluate(async () => {
    const progres = await (await fetch("/api/reward")).json();
    const tersedia = (progres.kupon ?? []).find(
      (k: { terpakai: boolean; berlaku: boolean }) => !k.terpakai && k.berlaku,
    );
    if (tersedia) return tersedia.kode_kupon;
    if (progres.poin_terkumpul < progres.poin_per_klaim) {
      // Poin habis pada DB pengembangan (tiap jalankan penuh memakai satu kupon) → skip.
      return null;
    }
    const res = await fetch("/api/reward/klaim", { method: "POST" });
    if (!res.ok) throw new Error("Gagal klaim kupon: jalankan `python seed.py` untuk isi poin");
    return (await res.json()).kode_kupon;
  });
  test.skip(!kode, "Poin reward di DB ini sudah terpakai; jalankan `python seed.py` lalu ulangi");

  // Isi keranjang lewat UI katalog
  const kartu = page.locator("article", { hasText: listing.nama });
  await expect(kartu.first()).toBeVisible();
  await kartu.first().getByRole("button", { name: `Add ${listing.nama} to cart` }).click();

  // Checkout dengan kode kupon
  await page.goto("/cart");
  await page.getByLabel("Coupon code").fill(kode!);
  await page.getByRole("button", { name: "Buy Now (1)" }).click();

  // Halaman pembayaran menampilkan total hasil penebusan kupon (potongan 10.000,
  // dibatasi 0 bila melebihi subtotal → tidak pernah negatif). Nilai harapan diambil
  // dari transaksi itu sendiri via API, bukan dihitung ulang dari harga listing.
  await expect(page).toHaveURL(/\/pembayaran\/\d+$/);
  const idTransaksi = page.url().match(/\/pembayaran\/(\d+)$/)?.[1] ?? "";
  const totalDiskon = await page.evaluate(async (id) => {
    return (await (await fetch(`/api/pembayaran/${id}`)).json()).total_harga as number;
  }, Number(idTransaksi));
  expect(totalDiskon).toBe(Math.max(0, listing.harga - 10_000));
  await expect(page.getByText(/ portion[s]? × Rp\. /).first()).toBeVisible();
  // "Total" dan angkanya berada di dua <span> terpisah, jadi asersi hanya pada angkanya.
  await expect(
    page.getByText(`Rp. ${totalDiskon.toLocaleString("id-ID")}`, { exact: true }),
  ).toBeVisible();
});

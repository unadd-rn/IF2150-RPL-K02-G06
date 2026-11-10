import { expect, test } from "@playwright/test";

test("buyer can only simulate payment with the payment button", async ({ page }) => {
  await page.goto("/login");
  await page.getByLabel("Email").fill("pembeli@test.com");
  await page.getByRole("textbox", { name: "Password" }).fill("password123");
  await page.getByRole("button", { name: "Log In" }).click();
  await expect(page).toHaveURL(/\/katalog$/);

  const transaksi = await page.evaluate(async () => {
    const katalogResponse = await fetch("/api/katalog");
    if (!katalogResponse.ok) throw new Error("Gagal memuat katalog");
    const katalog = await katalogResponse.json();
    if (!katalog.length) throw new Error("Katalog seed kosong");

    const checkoutResponse = await fetch("/api/pembayaran/checkout", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ items: [{ id_listing: katalog[0].id_listing, jumlah: 1 }] }),
    });
    if (!checkoutResponse.ok) throw new Error("Checkout gagal");
    return checkoutResponse.json();
  });

  await page.goto(`/pembayaran/${transaksi.id_transaksi}`);
  await expect(page.getByRole("img", { name: "QRIS dummy" })).toBeVisible();
  await expect(page.getByText("This demo QR code does not open a link or confirm payment when scanned.")).toBeVisible();
  const scanPage = await page.context().newPage();
  await scanPage.goto(transaksi.url_scan);
  await expect(scanPage.getByRole("heading", { name: "QR Scanning Is Disabled" })).toBeVisible();

  const statusBeforeSimulation = await page.evaluate(async (id) => {
    const response = await fetch(`/api/pembayaran/${id}`);
    return (await response.json()).status;
  }, transaksi.id_transaksi);
  expect(statusBeforeSimulation).toBe("MENUNGGU_BAYAR");

  await page.getByRole("button", { name: "Simulate Payment" }).click();
  await expect(page.getByRole("heading", { name: "Payment successful" })).toBeVisible();
  await expect(page.getByText("Pickup code")).toBeVisible();
  await scanPage.close();
});

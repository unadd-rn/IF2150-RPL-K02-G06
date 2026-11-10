import { expect, test } from "@playwright/test";

let createdListingName: string | null = null;

test.afterEach(async ({ page }) => {
  if (!createdListingName) return;
  await page.evaluate(async (nama) => {
    const response = await fetch("/api/listing/penjual");
    if (!response.ok) return;
    const listings = await response.json();
    await Promise.all(
      listings
        .filter((listing: { nama_makanan: string }) => listing.nama_makanan === nama)
        .map((listing: { id_listing: number }) =>
          fetch(`/api/listing/${listing.id_listing}`, { method: "DELETE" }),
        ),
    );
  }, createdListingName);
  createdListingName = null;
});

test("seller can log in and open listing management", async ({ page }) => {
  await page.goto("/login");
  await page.getByLabel("Email").fill(
    process.env.E2E_SELLER_EMAIL ?? "penjual@test.com",
  );
  await page.getByRole("textbox", { name: "Password" }).fill(
    process.env.E2E_SELLER_PASSWORD ?? "password123",
  );
  await page.getByRole("button", { name: "Log In" }).click();

  await expect(page).toHaveURL(/\/penjual$/);
  await page.getByRole("button", { name: "Manage Listings" }).click();
  await expect(page).toHaveURL(/\/penjual\/listing$/);
  await expect(
    page.getByRole("heading", { name: "Manage Listings" }),
  ).toBeVisible();
  await expect(
    page.getByRole("button", { name: "+ Add Listing" }),
  ).toBeVisible();

  await expect(
    page.getByText("Roti Tawar Penyelamatan").or(
      page.getByText("No food listings yet"),
    ),
  ).toBeVisible();

  await page.getByRole("button", { name: "+ Add Listing" }).click();
  await expect(page).toHaveURL(/\/penjual\/listing\/tambah$/);
  await expect(
    page.getByRole("heading", { name: "Add Product" }),
  ).toBeVisible();
  await expect(page.getByText("Product Photo*")).toBeVisible();
  await expect(page.getByLabel("Product Name *")).toBeVisible();
  await expect(page.getByLabel("Price (Rp) *")).toBeVisible();
  await expect(page.getByLabel("Stock *")).toBeVisible();
  await expect(page.getByLabel("Expiry Date *")).toBeVisible();
  await expect(page.getByRole("button", { name: "Show" })).toBeDisabled();

  await page.locator('input[type="file"]').setInputFiles("public/qris-dummy.png");
  const draftName = `E2E Listing Draft ${Date.now()}`;
  createdListingName = draftName;
  await page.getByLabel("Product Name *").fill(draftName);
  await page.getByLabel("Price (Rp) *").fill("12000");
  await page.getByLabel("Stock *").fill("2");
  await page.getByLabel("Description *").fill("Draf untuk verifikasi simpan dan terbitkan.");
  const kedaluwarsa = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000);
  kedaluwarsa.setMinutes(kedaluwarsa.getMinutes() - kedaluwarsa.getTimezoneOffset());
  await page.getByLabel("Expiry Date *").fill(kedaluwarsa.toISOString().slice(0, 16));
  await page.getByRole("button", { name: "Save Draft" }).click();

  await expect(page).toHaveURL(/\/penjual\/listing$/);
  await expect(page.getByRole("heading", { name: draftName })).toBeVisible();
  await expect(page.getByText("Draft", { exact: true }).first()).toBeVisible();
  await page.reload();
  await expect(page.getByRole("heading", { name: draftName })).toBeVisible();
  await expect(page.getByText("Draft", { exact: true }).first()).toBeVisible();

  const draftCard = page.locator(".group").filter({ has: page.getByRole("heading", { name: draftName }) });
  await draftCard.getByRole("button", { name: "Edit" }).click();
  await expect(page).toHaveURL(/\/penjual\/listing\/\d+\/edit$/);
  await page.getByRole("button", { name: "Save Changes / Show" }).click();

  await expect(page).toHaveURL(/\/penjual\/listing$/);
  await expect(page.getByRole("heading", { name: draftName })).toBeVisible();
  await expect(page.getByText("Available", { exact: true }).first()).toBeVisible();
});

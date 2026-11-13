import { expect, test } from "@playwright/test";

test("login page can show and hide the password", async ({ page }) => {
  await page.goto("/login");

  const password = page.locator('input[aria-label="Password"]');
  await password.fill("contoh-rahasia");
  await expect(password).toHaveAttribute("type", "password");

  await page.getByRole("button", { name: "Show password" }).click();
  await expect(password).toHaveAttribute("type", "text");

  await page.getByRole("button", { name: "Hide password" }).click();
  await expect(password).toHaveAttribute("type", "password");
});

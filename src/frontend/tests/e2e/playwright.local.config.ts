import { defineConfig, devices } from "@playwright/test";

// Config sementara (tidak untuk di-commit): memakai server dev milik proyek yang
// sudah berjalan di localhost:3000 (hostname "localhost"). baseURL bawaan proyek
// memakai 127.0.0.1 — Next.js 16 memblokir resource dev /_next/* dari Host yang
// tidak cocok, sehingga semua halaman kehilangan JS-nya saat test dari 127.0.0.1.
export default defineConfig({
  // config ini berada di dalam folder tests, jadi testDir yang benar = ".".
  testDir: ".",

  // Untan dev server lokal: jalankan berurutan supaya kompilasi Next dev +
  // login backend tidak berebut sumber daya (flaky bila 3 file paralel).
  workers: 1,
  timeout: 60_000,

  use: {
    ...devices["Desktop Chrome"],
    baseURL: "http://localhost:3000",
  },
  webServer: {
    command: "echo server sudah berjalan",
    url: "http://localhost:3000/login",
    reuseExistingServer: true,
    timeout: 30_000,
  },
});

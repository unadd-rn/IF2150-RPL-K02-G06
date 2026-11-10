import Link from "next/link";

export default function ScanPembayaranSuksesPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-[#e6e0c8] px-5 py-10">
      <section className="w-full max-w-md rounded-[18px] border border-[#d7d0b4] bg-[#f7f0dc] p-7 text-center shadow-sm">
        <h1 className="text-2xl font-black text-[#1b8ca3]">Payment successful</h1>
        <p className="mt-3 text-[#5d625b]">
          Payment has been received. The checkout screen will update automatically.
        </p>
        <Link
          href="/"
          className="mt-6 inline-flex min-h-12 items-center justify-center rounded-xl bg-[#f25f4b] px-6 py-3 font-bold text-white shadow-sm transition hover:brightness-110 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#d84b54]"
        >
          Back to home
        </Link>
      </section>
    </main>
  );
}

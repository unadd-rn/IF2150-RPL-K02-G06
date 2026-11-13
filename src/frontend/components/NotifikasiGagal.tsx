"use client";

type Props = { pesan: string | null; onClose: () => void };

export default function NotifikasiGagal({ pesan, onClose }: Props) {
  if (!pesan) return null;
  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/40 p-4" onClick={onClose}>
      <section
        role="alertdialog"
        aria-modal="true"
        aria-labelledby="notifikasi-gagal-title"
        aria-describedby="notifikasi-gagal-message"
        className="w-full max-w-md rounded-2xl border border-red-200 bg-[#fffaf0] p-6 shadow-xl"
        onClick={(event) => event.stopPropagation()}
      >
        <h2 id="notifikasi-gagal-title" className="text-xl font-bold text-red-700">Unable to continue</h2>
        <p id="notifikasi-gagal-message" className="mt-3 text-[#49483f]">{pesan}</p>
        <button type="button" autoFocus onClick={onClose} className="mt-5 rounded-lg bg-[#1a8ca1] px-5 py-2.5 font-bold text-white hover:brightness-110">
          Got it
        </button>
      </section>
    </div>
  );
}

"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { AppLayout } from "@/components/layout";
import TombolKeluar from "@/components/akun/TombolKeluar";
import { ambilProgresReward, klaimReward, ApiError, type ProgresReward } from "@/lib/api";

const rupiah = (n: number) => `Rp. ${n.toLocaleString("id-ID")}`;
const hariIni = () => new Date().toLocaleDateString("en-CA"); // YYYY-MM-DD, local time

export default function RewardPage() {
  const [data, setData] = useState<ProgresReward | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [perluLogin, setPerluLogin] = useState(false);
  const [mengklaim, setMengklaim] = useState(false);
  const [pesan, setPesan] = useState<{ jenis: "ok" | "gagal"; teks: string } | null>(null);
  // new Date() tidak stabil saat prerender, jadi dihitung di client saja (useEffect).
  const [tanggalHariIni, setTanggalHariIni] = useState<string | null>(null);

  useEffect(() => {
    setTanggalHariIni(hariIni());
  }, []);

  const muat = useCallback(async () => {
    try {
      setError(null);
      setData(await ambilProgresReward());
    } catch (e) {
      if (e instanceof ApiError && (e.status === 401 || e.status === 403)) setPerluLogin(true);
      setError(e instanceof ApiError ? e.message : "Could not load rewards");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    muat();
  }, [muat]);

  async function onKlaim() {
    setMengklaim(true);
    setPesan(null);
    try {
      const kupon = await klaimReward();
      setPesan({ jenis: "ok", teks: `Coupon ${kupon.kode_kupon} claimed successfully!` });
      await muat();
    } catch (e) {
      if (e instanceof ApiError && e.status === 400) {
        setPesan({ jenis: "gagal", teks: "You do not have enough points to claim a coupon." });
      } else if (e instanceof ApiError && e.status >= 500) {
        setPesan({ jenis: "gagal", teks: "The system could not process your claim. Please try again later." });
      } else {
        setPesan({ jenis: "gagal", teks: e instanceof ApiError ? e.message : "An error occurred" });
      }
    } finally {
      setMengklaim(false);
    }
  }

  const persen = data ? Math.min(100, (data.poin_terkumpul / data.poin_per_klaim) * 100) : 0;
  const sudahLoginHariIni = tanggalHariIni !== null && data?.tanggal_login_terakhir === tanggalHariIni;

  return (
    <AppLayout
      role="buyer"
      isAuthenticated
      title={<h1 className="text-2xl font-bold text-[#fff4f2] text-center sm:text-4xl">My Reward</h1>}
      showHeader
      theme="pink"
      headerClassName="px-5 pb-5 pt-8"
      bodyClassName="bg-[#e6e0c8] px-4 py-5"
    >
      <div className="space-y-5">
        {loading && <p className="text-center text-[#7a705c]">Loading rewards...</p>}

        {!loading && error && (
          <div className="rounded-[18px] bg-[#f4efe3] p-4 text-center shadow-sm">
            <p className="font-medium text-red-600">{error}</p>
            {perluLogin ? (
              <Link href="/login" className="mt-2 inline-block underline">
                Log in first
              </Link>
            ) : (
              <button onClick={muat} className="mt-3 rounded-full bg-[#f56369] px-5 py-2 font-bold text-white">
                Try again
              </button>
            )}
          </div>
        )}

        {data && (
          <>
            {/* Progress */}
            <div className="rounded-[20px] bg-[#f6f0de] p-4 text-center shadow-sm">
              <div className="mb-4 flex justify-center">
                <div className="flex h-32 w-44 items-center justify-center rounded-full bg-[#f1d69a] text-5xl shadow-inner">
                  🥚
                </div>
              </div>

              <h3 className="text-[1.6rem] font-black tracking-[-0.03em] text-[#f15a62]">
                {sudahLoginHariIni ? "Already logged in today ✓" : "Log in every day to earn points"}
              </h3>
              <p className="mt-1 text-sm text-[#7a705c]">
                +{data.poin_per_login} points for your first log in each day
                {data.tanggal_login_terakhir && ` · Last log in: ${data.tanggal_login_terakhir}`}
              </p>
            </div>

            {/* Points + claim */}
            <div className="space-y-4 rounded-[18px] bg-[#f4efe3] p-4 shadow-sm">
              <div className="flex items-center justify-between text-[1.7rem] font-black text-[#1d9eb8]">
                <span>Total Points</span>
                <span>{data.poin_terkumpul}</span>
              </div>

              <div>
                <div className="h-3 w-full overflow-hidden rounded-full bg-[#ddd3bb]">
                  <div className="h-full rounded-full bg-[#1d9eb8] transition-all" style={{ width: `${persen}%` }} />
                </div>
                <p className="mt-1 text-right text-sm text-[#7a705c]">
                  {data.poin_terkumpul} / {data.poin_per_klaim} points
                </p>
              </div>

              <button
                onClick={onKlaim}
                disabled={mengklaim}
                className="w-full rounded-full bg-[#f56369] py-3 text-lg font-bold text-white transition hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {mengklaim
                  ? "Processing..."
                  : `Claim ${rupiah(data.nilai_potongan)} Coupon (${data.poin_per_klaim} points)`}
              </button>

              {pesan && (
                <p className={`text-sm font-medium ${pesan.jenis === "ok" ? "text-green-700" : "text-red-600"}`}>
                  {pesan.teks}
                </p>
              )}
            </div>

            {/* Coupons */}
            <div className="space-y-3">
              <h4 className="text-xl font-black text-[#1d1d1d]">My Coupons</h4>

              {data.kupon.length === 0 && (
                <p className="text-sm text-[#7a705c]">
                  No coupons yet. Collect {data.poin_per_klaim} points to claim one.
                </p>
              )}

              {data.kupon.map((k) => (
                <div
                  key={k.kode_kupon}
                  className={`rounded-[18px] px-5 py-4 text-white shadow-sm ${k.berlaku ? "bg-[#f8b638]" : "bg-[#c7bba0]"}`}
                >
                  <div className="flex items-center justify-between gap-3">
                    <span className="text-[1.8rem] font-black">{rupiah(k.nilai_potongan)}</span>
                    <div className="text-right">
                      <div className="font-mono text-base font-bold">{k.kode_kupon}</div>
                      <div className="text-sm opacity-90">Valid until: {k.berlaku_sampai}</div>
                      {!k.berlaku && (
                        <span className="mt-1 inline-block rounded-full bg-white/30 px-2 text-xs font-bold">
                          {k.terpakai ? "Used" : "Expired"}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}

        <TombolKeluar />
      </div>
    </AppLayout>
  );
}

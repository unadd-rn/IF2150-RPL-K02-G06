import type { Metadata } from "next";
import { Suspense } from "react";
import { AppLayout } from "@/components/layout";
import DetailListing from "@/components/katalog/DetailListing";
import PesanKatalog from "@/components/katalog/PesanKatalog";

export const metadata: Metadata = { title: "Listing Details" };

export default function DetailListingPage() {
  return (
    <AppLayout
      role="buyer"
      isAuthenticated
      title={<h1 className="text-2xl font-bold text-[#fff4f2] text-center sm:text-4xl">Listing Details</h1>}
      showHeader
      theme="green"
      headerClassName="px-5 pb-4 pt-8"
      bodyClassName="px-4 py-5 lg:px-6"
    >
      <div className="mx-auto w-full max-w-5xl">
        <Suspense fallback={<PesanKatalog>Loading listing details…</PesanKatalog>}>
          <DetailListing />
        </Suspense>
      </div>
    </AppLayout>
  );
}

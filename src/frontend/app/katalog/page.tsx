import type { Metadata } from "next";
import { Suspense } from "react";
import { AppLayout } from "@/components/layout";
import DaftarListing from "@/components/katalog/DaftarListing";
import FormPencarian from "@/components/katalog/FormPencarian";
import PesanKatalog from "@/components/katalog/PesanKatalog";

export const metadata: Metadata = { title: "Surplus Food Catalog" };

export default function KatalogPage() {
  return (
    <AppLayout
      role="buyer"
      isAuthenticated
      title={<h1 className="text-2xl font-bold text-[#fff4f2] text-center sm:text-4xl">Today's Menu</h1>}
      showHeader
      theme="green"
      headerClassName="px-5 pb-4 pt-4"
      bodyClassName="px-4 py-5 lg:px-6"
    >
      <div className="mx-auto w-full max-w-6xl">
        <Suspense fallback={<PesanKatalog>Loading catalog…</PesanKatalog>}>
          <div className="space-y-5">
            <FormPencarian />
            <DaftarListing />
          </div>
        </Suspense>
      </div>
    </AppLayout>
  );
}

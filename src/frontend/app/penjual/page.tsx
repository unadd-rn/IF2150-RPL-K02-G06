import { AppLayout } from "@/components/layout";

export default function SellerDashboardPage() {
  return (
    <AppLayout
      role="seller"
      isAuthenticated
      title="Seller Dashboard"
      showHeader
      headerClassName="bg-[#1bb0c7] px-5 pb-5 pt-8"
      bodyClassName="bg-[#e6e0c8] px-4 py-5"
    >
      <div className="space-y-4 pb-4">
        <div className="rounded-[18px] bg-[#f7f0dc] p-4 shadow-sm">
          <p className="text-sm uppercase tracking-[0.12em] text-[#60756b]">Today</p>
          <h3 className="mt-2 text-3xl font-black text-[#1a8ca1]">12 Listings</h3>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div className="rounded-[18px] bg-[#fffaf0] p-4 shadow-sm">
            <p className="text-sm text-[#60756b]">Orders</p>
            <p className="mt-2 text-3xl font-black text-[#f15d69]">46</p>
          </div>
          <div className="rounded-[18px] bg-[#fffaf0] p-4 shadow-sm">
            <p className="text-sm text-[#60756b]">Revenue</p>
            <p className="mt-2 text-3xl font-black text-[#1b8ca3]">Rp 3.2M</p>
          </div>
        </div>
      </div>
    </AppLayout>
  );
}

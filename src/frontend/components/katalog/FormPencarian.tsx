"use client";

import Form from "next/form";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import FilterHarga from "./FilterHarga";
import SearchBar from "./SearchBar";
import { adaPencarian, bacaPencarian } from "./pencarian";

/**
- Form cari & filter harga (UC04). Submit = GET /katalog?kata_kunci=&harga_min=&harga_maks=,
- lalu DaftarListing membaca URL dan menjalankan kirimPencarian.
 */
export default function FormPencarian() {
  const searchParams = useSearchParams();
  const pencarian = bacaPencarian(searchParams);

  return (
    // key: isi ulang defaultValue saat URL berubah (mis. tombol back / reset)
    <Form
      key={searchParams.toString()}
      action="/katalog"
      role="search"
      className="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center"
    >
      {/* w-full on mobile, and flex-1 on sm+ so the search bar always gets
          the leftover width — wider than the fixed-content filter harga */}
      <div className="w-full sm:flex-1">
        <SearchBar defaultValue={pencarian.kataKunci} />
      </div>

      <FilterHarga hargaMin={pencarian.hargaMin} hargaMaks={pencarian.hargaMaks} />
      
      <div className="flex gap-2 items-center">
        <button
          type="submit"
          className="flex-1 sm:flex-none h-[50px] px-6 rounded-[18px] bg-emerald-600 font-semibold text-white hover:bg-emerald-700 flex items-center justify-center shadow-sm"
        >
          Search
        </button>
        {adaPencarian(pencarian) && (
          <Link
            href="/katalog"
            className="flex-1 sm:flex-none h-[50px] px-6 rounded-[18px] border border-[#d8d0b7] bg-[#f3ebd9] text-[#58655d] text-center font-medium hover:bg-[#eae2ce] flex items-center justify-center shadow-sm"
          >
            Reset
          </Link>
        )}
      </div>
    </Form>
  );
}

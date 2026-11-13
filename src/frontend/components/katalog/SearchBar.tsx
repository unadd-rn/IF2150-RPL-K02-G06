import { PARAM_KATA_KUNCI } from "./pencarian";

/** Kolom kata kunci nama makanan (UC04). */
export default function SearchBar({ defaultValue }: { defaultValue?: string | null }) {
  return (
    <label className="flex flex-1 items-center gap-3 rounded-[18px] border border-[#d8d0b7] bg-[#f3ebd9] px-4 py-3 text-[#58655d] shadow-sm">
      <svg viewBox="0 0 24 24" className="h-5 w-5 fill-none stroke-current stroke-[2]" aria-hidden="true">
        <circle cx="11" cy="11" r="5.5" />
        <path d="M16 16l4.4 4.4" strokeLinecap="round" />
      </svg>
      <input
        type="search"
        name={PARAM_KATA_KUNCI}
        defaultValue={defaultValue ?? ""}
        placeholder="Search food name"
        className="w-full bg-transparent text-base text-[#1f201d] placeholder:text-[#5f665e] focus:outline-none"
      />
    </label>
  );
}

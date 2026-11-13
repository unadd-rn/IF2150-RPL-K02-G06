import { PARAM_HARGA_MAKS, PARAM_HARGA_MIN } from "./pencarian";

const kelasInput =
  "w-full bg-transparent text-base text-[#1f201d] placeholder:text-[#5f665e] focus:outline-none";

const kelasKotak =
  "flex flex-1 items-center gap-3 rounded-[18px] border border-[#d8d0b7] bg-[#f3ebd9] px-4 py-3 text-[#58655d] shadow-sm";

export default function FilterHarga({
  hargaMin,
  hargaMaks,
}: {
  hargaMin?: number | null;
  hargaMaks?: number | null;
}) {
  return (
    <fieldset className="flex gap-3 text-sm">
      <legend className="sr-only">Price range</legend>
      
      <label className={`${kelasKotak} h-[50px]`}>
        <svg viewBox="0 0 24 24" className="h-5 w-5 fill-none stroke-current stroke-[2] shrink-0" aria-hidden="true">
          <path d="M4 19h16M4 15h16M4 11h16M4 7h16" strokeLinecap="round" />
        </svg>
        <div className="flex w-full flex-col justify-center">
          <span className="text-[10px] font-medium leading-tight text-[#5f665e]">Min price (Rp)</span>
          <input
            type="number"
            name={PARAM_HARGA_MIN}
            min={0}
            step={1}
            inputMode="numeric"
            defaultValue={hargaMin ?? ""}
            placeholder="0"
            className={kelasInput}
          />
        </div>
      </label>

      <label className={`${kelasKotak} h-[50px]`}>
        <svg viewBox="0 0 24 24" className="h-5 w-5 fill-none stroke-current stroke-[2] shrink-0" aria-hidden="true">
          <path d="M4 19h16M4 15h16M4 11h16M4 7h16" strokeLinecap="round" />
        </svg>
        <div className="flex w-full flex-col justify-center">
          <span className="text-[10px] font-medium leading-tight text-[#5f665e]">Max price (Rp)</span>
          <input
            type="number"
            name={PARAM_HARGA_MAKS}
            min={0}
            step={1}
            inputMode="numeric"
            defaultValue={hargaMaks ?? ""}
            placeholder="Tanpa batas"
            className={kelasInput}
          />
        </div>
      </label>
    </fieldset>
  );
}

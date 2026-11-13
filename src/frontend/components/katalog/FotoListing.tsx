"use client";

import { useState } from "react";
import { urlFoto } from "@/lib/api";

type Props = { foto: string | null; alt: string; className?: string };

export default function FotoListing({ foto, alt, className = "" }: Props) {
  const [gagal, setGagal] = useState(false);
  const src = urlFoto(foto);

  if (!src || gagal) {
    return (
      <div className={`flex items-center justify-center bg-zinc-100 text-sm text-zinc-400 dark:bg-zinc-800 ${className}`}>
        No photo available
      </div>
    );
  }
  // <img> biasa: foto berasal dari backend (host lain), tanpa perlu konfigurasi remotePatterns
  // eslint-disable-next-line @next/next/no-img-element
  return <img src={src} alt={alt} onError={() => setGagal(true)} className={`object-cover ${className}`} />;
}

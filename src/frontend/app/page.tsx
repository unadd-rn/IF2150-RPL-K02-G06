import { cookies } from "next/headers";
import { redirect } from "next/navigation";

export const instant = false;

export default async function HomePage() {
  const cookieStore = await cookies();
  const role = cookieStore.get("role")?.value;

  if (role === "PEMBELI") {
    redirect("/katalog");
  }

  if (role === "PENJUAL") {
    redirect("/penjual");
  }

  redirect("/login");
}

"use client";

import { useState, type ChangeEvent, type FormEvent } from "react";
import { useRouter } from "next/navigation";
import Image from "next/image";
import { AppLayout } from "@/components/layout";
import { IMAGES } from "@/constants/assets"; // <-- 1. Import your assets

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [showPassword, setShowPassword] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string>("");
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);

  const handleEmailChange = (event: ChangeEvent<HTMLInputElement>) => {
    setEmail(event.target.value);
  };

  const handlePasswordChange = (event: ChangeEvent<HTMLInputElement>) => {
    setPassword(event.target.value);
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setErrorMessage("");
    setIsSubmitting(true);

    try {
      const response = await fetch("/api/auth/login", {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json().catch(() => null);

      if (!response.ok) {
        const message = "Log in failed. Please check your details and try again.";
        setErrorMessage(message);
        return;
      }

      const role = data?.peran;
      if (role === "PENJUAL") {
        router.push("/penjual");
        return;
      }

      router.push("/katalog");
    } catch {
      setErrorMessage("Log in failed. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <AppLayout
      showHeader
      showBottomNav={false}
      title={
        <div className="flex w-full items-center justify-center py-1">
          <Image
            src={IMAGES.logo}
            alt="Surplus Logo"
            width={140}  // Increased base width
            height={45}  // Increased base height
            className="h-40 md:h-50 w-auto object-contain" // Tailwind classes for sizing and scaling
            priority
          />
        </div>
      }
      headerClassName="bg-[#f4b61a] px-5 pb-5 pt-8"
      bodyClassName="bg-[#f8f4d0] px-5 pb-10 pt-4"
    >
      <div className="flex min-h-full flex-col justify-center">
        <h2 className="mb-8 text-center text-[2.3rem] font-black tracking-[-0.06em] text-[#f15d69]">
          Log In Your Account
        </h2>

        {errorMessage ? (
          <div className="mb-4 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
            {errorMessage}
          </div>
        ) : null}

        <form onSubmit={handleSubmit} className="space-y-4">
          <label className="flex items-center gap-3 rounded-lg bg-[#e6d9aa] px-4 py-3 text-[#716759] shadow-inner">
            <svg viewBox="0 0 24 24" className="h-6 w-6 fill-none stroke-current stroke-[1.8]" aria-hidden="true">
              <path d="M4 7.5A2.5 2.5 0 0 1 6.5 5h11A2.5 2.5 0 0 1 20 7.5v9A2.5 2.5 0 0 1 17.5 19h-11A2.5 2.5 0 0 1 4 16.5v-9Z" />
              <path d="m5 7 7 5 7-5" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
            <input
              type="email"
              value={email}
              onChange={handleEmailChange}
              placeholder="Enter Your Email"
              className="w-full bg-transparent text-base text-[#211f1d] placeholder:text-[#6d7268] focus:outline-none"
              aria-label="Email"
              required
            />
          </label>

          <label className="flex items-center gap-3 rounded-lg bg-[#e6d9aa] px-4 py-3 text-[#716759] shadow-inner">
            <svg viewBox="0 0 24 24" className="h-6 w-6 fill-none stroke-current stroke-[1.8]" aria-hidden="true">
              <rect x="5" y="10" width="14" height="10" rx="2" />
              <path d="M8 10V7.5A4 4 0 0 1 12 3.5a4 4 0 0 1 4 4V10" strokeLinecap="round" />
            </svg>
            <input
              type={showPassword ? "text" : "password"}
              value={password}
              onChange={handlePasswordChange}
              placeholder="Enter Your Password"
              className="w-full bg-transparent text-base text-[#211f1d] placeholder:text-[#6d7268] focus:outline-none"
              aria-label="Password"
              required
            />
            <button
              type="button"
              onClick={() => setShowPassword((value) => !value)}
              aria-label={showPassword ? "Hide password" : "Show password"}
              className="text-[#716759] hover:text-[#39423c]"
            >
              {showPassword ? (
                <svg
                  viewBox="0 0 24 24"
                  className="h-5 w-5 fill-none stroke-current stroke-[1.8]"
                  aria-hidden="true"
                >
                  <path d="M3 3l18 18" strokeLinecap="round" />
                  <path
                    d="M10.6 10.6a2 2 0 0 0 2.8 2.8"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                  <path
                    d="M9.9 5.3A10.6 10.6 0 0 1 12 5c5.6 0 9.2 4.8 9.8 6-.3.7-1.8 3-4.2 4.7"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                  <path
                    d="M6.3 7.1C4.1 8.7 2.6 10.9 2.2 11.8 2.8 13 6.4 17.8 12 17.8c.8 0 1.6-.1 2.3-.2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              ) : (
                <svg
                  viewBox="0 0 24 24"
                  className="h-5 w-5 fill-none stroke-current stroke-[1.8]"
                  aria-hidden="true"
                >
                  <path
                    d="M2 12C4 8.5 7.5 6 12 6s8 2.5 10 6c-2 3.5-5.5 6-10 6S4 15.5 2 12Zm10-3a3 3 0 1 0 0 6 3 3 0 0 0 0-6Z"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                  <circle cx="12" cy="12" r="3" />
                </svg>
              )}
            </button>
          </label>

          <button
            type="submit"
            disabled={isSubmitting}
            className="mt-4 w-full rounded-lg bg-[#1dbf75] px-5 py-4 text-2xl font-black text-white transition hover:bg-[#17a366] disabled:cursor-not-allowed disabled:opacity-70"
          >
            {isSubmitting ? "Logging in..." : "Log In"}
          </button>
        </form>
      </div>
    </AppLayout>
  );
}

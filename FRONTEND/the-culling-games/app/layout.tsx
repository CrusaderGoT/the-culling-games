import type { Metadata } from "next";
import "./globals.css";
import { inter, lusitana } from "./fonts";
import Image from "next/image";

export const metadata: Metadata = {
  title: "The Culling Games",
  description: "Generated by create next app",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.className} antialiased min-w-[200px] pt-[60px]`}>
        <Header />
        {children}
      </body>
    </html>
  );
}

function Header() {
  return (
    <header className={`fixed bg-gradient-to-l dark:bg-gradient-to-r from-black via-gray-500 to-white top-0 z-20 w-full flex justify-center h-fit min-h-[50px] max-h-[60px] p-1`}>
      <div className="flex w-[60%] items-center gap-3 justify-between">

        <KoganeImg />

        <div>
          <p className={`${lusitana.className} max-h-[60px] font-bold text-sm sm:text-lg md:text-xl lg:text-2xl tracking-wide md:tracking-wider lg:tracking-widest`}>
            The Culling Games
          </p>
        </div>

        <KoganeImg />

      </div>
    </header>
  );
}

export function KoganeImg() {
  return (
    <Image
      src="/images/Kogane.png"
      alt="Kogane-Header.png"
      width={325}
      height={275}
      className={`h-[50px] w-[50px]`}
    />
  )
}
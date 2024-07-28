import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { Lusitana } from "next/font/google";
import { Courier_Prime } from "next/font/google";
import "./globals.css";

// Global Fonts
const inter = Inter({ subsets: ["latin"] });
export const lusitana = Lusitana({
  weight: ['400', '700'],
  subsets: ["latin"]
});
export const courier = Courier_Prime({
  weight: ["400", "700"],
  subsets: ["latin", "latin-ext"]
});

export const metadata: Metadata = {
  title: "The Culling Games",
  description: "add html description later",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.className} antialiased`}>
        {children}
      </body>
    </html>
  );
}

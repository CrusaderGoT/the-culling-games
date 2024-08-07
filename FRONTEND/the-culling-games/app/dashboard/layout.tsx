// layouts for the dashboard
'use client'
import Link from "next/link";
import { usePathname } from "next/navigation";
import { links } from "./links";
import Image from "next/image";

export default function Layout({ children }: { children: React.ReactNode }) {
    return (
			<main className="h-screen w-full my-auto flex flex-col md:flex-row">
				<SideNav />
				{children}
			</main>
    );
  }

  function SideNav() {
	const pathname = usePathname();
	console.log(pathname)
	return (
			<div className="flex relative justify-around md:justify-normal gap-1 md:flex-col md:w-[25%] md:h-full overflow-hidden md:gap-2">
			{links.map((link) => {
			return (
				<Link
					key={link.name}
					href={link.href}
					className={`${link.name === "log out" ? "hidden md:flex absolute mb-2 bg-transparent bottom-0": ""} h-[40px] w-full flex justify-center md:justify-start items-center ${pathname === '/dashboard' ? 'absolukte' : ''} rounded-t-md md:rounded-md bg-slate-500 p-3 text-sm font-medium`}
				>
					<Image 
					src={link.icon}
					alt={link.name}
					width={link.iconWidth}
					height={link.iconHeight}
					className="hidden md:block h-fit w-[20px] mr-1"
					/>
					<p className="h-fit text-end">{link.name}</p>
				</Link>
			);
			})}
			</div>    
		);
}
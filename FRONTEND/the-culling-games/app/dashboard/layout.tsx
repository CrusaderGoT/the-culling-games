// layouts for the dashboard
'use client'
import Link from "next/link";
import { usePathname } from "next/navigation";
import { links } from "./links";
import Image from "next/image";

export default function Layout({ children }: { children: React.ReactNode }) {
    return (
			<main className="min-w-[250px] relative sm:h-[100vh] w-full flex flex-col md:flex-row pt-[100px]">
				<SideNav />
				{children}
			</main>
    );
  }

  function SideNav() {
	const pathname = usePathname();
	return (
			<div className="flex sticky top-[0px] justify-around z-20
			md:justify-normal md:flex-col md:w-[25%] md:h-full backdrop-blur-xl
			md:gap-4 gap-2 border-b border-slate-900 md:max-w-[20%]">
			{links.map((link) => {
			return (
				<Link
					key={link.name}
					title={link.name}
					href={link.href}
					className={`${link.name === "log out" ? "hidden md:flex absolute mb-2 bg-transparent bottom-0": ""}
					flex max-h-[25px] items-center rounded-t-md md:rounded-md
					p-1 md:p-2 text-sm font-medium bg-gradient-radial to-100% 
					${link.href === pathname ? "from-orange-400 to-green-400" : "from-teal-400 to-red-400"}`}
				>
					<Image 
					src={link.icon}
					alt={link.name}
					width={link.iconWidth}
					height={link.iconHeight}
					className="w-[10px] h-[10px] md:w-[20px] md:h-[20px]"
					/>
					<p className="hidden md:block">{link.name}</p>
				</Link>
			);
			})}
			</div>    
		);
}
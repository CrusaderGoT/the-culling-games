// layouts for the dashboard
'use client'
import Link from "next/link";
import clsx from 'clsx';
import { usePathname } from "next/navigation";

export default function Layout({ children }: { children: React.ReactNode }) {
    return (
			<>
			<main className="flex h-screen pt-[100px] border border-red-600">
			<SideNav />
				<div className="flex-grow p-6 md:overflow-y-auto md:p-12">{children}</div>
			</main>
			</>
    );
  }

function SideNav() {
	const pathname = usePathname();
	return (
		<div className="w-full flex-none md:w-64 h-fit md:h-full border">
			<div className="flex justify-around md:flex-col overflow-hidden md:gap-12">

				<Link
				href={`http://localhost:3000/dashboard/player`}
				>
					Player
				</Link>
				
				

			</div>
		</div>     
	);
}
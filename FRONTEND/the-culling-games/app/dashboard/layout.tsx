// layouts for the dashboard
"use client";
import { links } from "./links";
import { NavButton } from "@/components/NavButton";
import { usePathname } from "next/navigation";

export default function Layout({ children }: { children: React.ReactNode }) {
    return (
        <div className="w-full h-full flex flex-col md:flex-row gap-2">
            <SideNav />
            {children}
        </div>
    );
}

/**
 * SideNav component renders a side navigation bar with links.
 * The navigation bar is responsive and adjusts its layout based on the screen size.
 *
 * returns {JSX.Element} The rendered side navigation component.
 *
 * @remarks
 * - The component uses `usePathname` to get the current path and highlight the active link.
 * - The links are rendered from a `links` array, each containing `name`, `href`, `icon`, `iconWidth`, and `iconHeight`.
 * - The "log out" link is hidden on smaller screens and positioned at the bottom on larger screens.
 * - The component uses Tailwind CSS classes for styling and responsiveness.
 */
function SideNav() {
    const pathname = usePathname();
    return (
        <div
            className="flex sticky top-[60px] justify-evenly z-20
			md:flex-col md:w-[25%] md:h-svh backdrop-blur-sm
			border-t p-1
			md:gap-4 gap-2 border-b border-slate-900 md:max-w-[20%]"
        >
            {links.map((link, inx) => {
                return (
                    <NavButton
                        href={link.href}
                        icon={link.icon}
                        label={link.name}
                        key={inx}
                        className={`bg-gradient-radial to-100% ${
                            link.href === pathname
                                ? "from-blue-500 to-purple-500"
                                : "from-gray-200 to-gray-400"
                        } w-max h-max p-1
`}
                    />
                );
            })}
        </div>
    );
}

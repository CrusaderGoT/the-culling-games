import { LucideIcon } from "lucide-react";
import { Button } from "./ui/button";
import Link from "next/link";
import { usePathname } from "next/navigation";

type Props = {
    icon: LucideIcon,
    label: string,
    href?: string,
    className?: string,
}

export function NavButton({
    icon: Icon,
    label,
    href,
    className,
}: Props) {
    return (
        <Button
            variant={"ghost"}
            size={"icon"}
            aria-label={label}
            title={label}
            className={`rounded-full ${className}`}
            asChild
        >
            {href ? (
                <Link href={href}>
                <Icon />
                </Link>
            ): (
                <Icon />
            )}
        </Button>
    )
    
}

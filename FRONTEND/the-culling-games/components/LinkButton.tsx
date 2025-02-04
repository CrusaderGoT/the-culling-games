import { LucideIcon } from "lucide-react";
import { Button } from "./ui/button";
import Link from "next/link";

type Props = {
    icon: LucideIcon,
    label: string,
    href?: string,
}

export function LinkButton({
    icon: Icon,
    label,
    href,

}: Props) {
    return (
        <Button
            variant={"secondary"}
            aria-label={label}
            title={label}
        >
            {href ? (
                <Link href={href}>
                <div className="hidden sm:flex gap-1 place-content-center">{label}<Icon /></div>
                <div className="sm:hidden text-center">{label}</div>
                </Link>
            ): (
                <Icon />
            )}
        </Button>
    )
    
}
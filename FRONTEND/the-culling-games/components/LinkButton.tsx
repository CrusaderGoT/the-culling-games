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
                <Link href={href} className="flex text-center gap-1">
                    {label}
                    <div className="hidden sm:block"><Icon /></div>
                </Link>
            ): (
                <Icon />
            )}
        </Button>
    )
    
}
import { LucideIcon } from "lucide-react";
import { Button } from "./ui/button";
import Link from "next/link";
import { ButtonHTMLAttributes } from "react";

type Props = {
    icon: LucideIcon,
    label: string,
    href?: string,
} & ButtonHTMLAttributes<HTMLButtonElement>

export function LinkButton({
    icon: Icon,
    label,
    href,
    ...props

}: Props) {
    return (
        <Button
            {...props}
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
"use client";

import { lusitana } from "@/app/fonts";
import Image from "next/image";
import * as React from "react";
import { Moon, Sun } from "lucide-react";
import { useTheme } from "next-themes";
import { Button } from "@/components/ui/button";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

export function Header() {
    return (
        <header
            className={`fixed min-w-[250px] bg-gradient-to-b from-[hsla(0,0%,0%,50%)]
      dark:from-[hsla(0,0%,0%,100%)] to-transparent
      top-0 z-[100] w-full h-fit min-h-[50px]
      max-h-[60px] p-1`}
        >
            <div className="flex justify-center items-center relative">
                <div className="flex items-center gap-3 justify-between">
                    <KoganeImg />

                    <div>
                        <p
                            className={`${lusitana.className} max-h-[60px] font-bold text-sm sm:text-lg md:text-xl lg:text-2xl tracking-wide md:tracking-wider lg:tracking-widest text-nowrap`}
                        >
                            The Culling Games
                        </p>
                    </div>

                    <KoganeImg />
                </div>
                <span className="absolute right-0 z-10">
                    <ModeToggle />
                </span>
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
    );
}

export function ModeToggle() {
    const { setTheme } = useTheme();

    return (
        <DropdownMenu>
            <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="icon" className="rounded-full">
                    <Sun className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
                    <Moon className="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
                    <span className="sr-only">Toggle theme</span>
                </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
                <DropdownMenuItem onClick={() => setTheme("light")}>
                    Light
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => setTheme("dark")}>
                    Dark
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => setTheme("system")}>
                    System
                </DropdownMenuItem>
            </DropdownMenuContent>
        </DropdownMenu>
    );
}

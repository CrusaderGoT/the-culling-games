"use client";
import Image from "next/image";
import * as React from "react";

interface KoganeImageProp {
    className?: string
}

export function KoganeImage({ className }: KoganeImageProp) {
    return (
        <Image
            src="/images/Kogane.png"
            alt="Kogane-Header.png"
            width={325}
            height={275}
            priority
            aschild="true"
            className={`h-[50px] w-[50px] ${className}`} />
    );
}

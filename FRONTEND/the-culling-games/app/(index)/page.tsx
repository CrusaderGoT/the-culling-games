"use client";

import Image from "next/image";
import index from "./index.module.css";
import { useRouter } from "next/navigation";

export default function Home() {
    return (
        <div
            className="
            bg-gradient-rzadial dark:from-slate-400 dark:to-slate-900 to-slate-400 from-slate-900
            font-mono text-sm flex items-center min-h-screen
            justify-center relative"
        >
            <ColonyCircle />
        </div>
    );
}

function ColonyCircle() {
    return (
        <div
            className={`${index.colonyCircle} p-5 overflow-hidden
      w-[380px] h-[380px]
      sm:w-[600px] sm:h-[600px]
      md:w-[700px] md:h-[700px]
      rounded-full cursor-default
      relative flex items-center justify-center
      container
      `}
        >
            <ColonyBarrier />
            <ColonyImg />
            <CircleContent />
        </div>
    );
}

function ColonyBarrier() {
    return (
        <div
            className={`${index.colonyBarrier} bg-[hsla(0,0%,0%,97%)]
    absolute min-w-full min-h-full z-[4] rounded-full`}
        ></div>
    );
}

function ColonyImg() {
    return (
        <Image
            src={`/images/images.jpeg-1.jpg`}
            alt="city-skyline.jpg"
            width={612}
            height={408}
            className="absolute w-full h-full rounded-full"
            priority={false}
        />
    );
}

function CircleContent() {
    return (
        <div className="relative !text-white z-[6] rounded-full flex flex-col items-center justify-center w-full h-full">
            <ColonyText />
            <ColonyWarning />
            <EnterBtn />
        </div>
    );
}

function ColonyText() {
    return (
        <h2
            className={`${index.colonyText} font-semibold
      sm:font-bold lg:font-extrabold tracking-[10px]
      md:tracking-[20px] lg:tracking-[30px]
      text-lg sm:text-2xl md:text-3xl
      absolute top-1/2 translate-y-[-50%]`}
        >
            COLONY
        </h2>
    );
}

function ColonyWarning() {
    return (
        <p
            className={`${index.colonyWarn} absolute bottom-2 text-[10px]
      leading-3 sm:text-xs text-wrap
      text-center w-2/3 text-red-600 font-thin`}
        >
            a dangerous game is going on inside &#x1F6C8;
        </p>
    );
}

function EnterBtn() {
    const router = useRouter();
    return (
        <button
            onClick={() => router.push("/dashboard")}
            type="button"
            className={`${index.colonyBtn} opacity-0 absolute bottom-[25%]
        h-[12px] w-[32px] sm:h-[20px] sm:w-[50px] rounded-full
        text-[9px] sm:text-[12px] md:text-base font-semibold
        tracking-wider flex items-center justify-center
        bg-gradient-conic from-slate-600 via-slate-900 to-black`}
        >
            YES
        </button>
    );
}

"use client"

import { lusitana } from "@/app/fonts";
import Image from "next/image";

export default function PlayerPage() {
    return (
        <div className="flex h-full w-full p-3 overflow-y-auto">
            <ListOfPlayers />
        </div>
    );
}

function ListOfPlayers() {
    return (
        <div
            className=" flex flex-row gap-4 flex-wrap
    "
        > <PlayerCard /></div>
    );
}

export function PlayerCard() {
    return (
        <div
            className="p-1 bg-gradient-to-tr from-[hsl(73,84%,60%)] to-emerald-400
      dark:bg-gradient-to-bl dark:from-indigo-600 dark:to-violet-900 dark:text-white
      rounded-md w-full h-max max-w-[280px] sm:max-w-[300px] sm:max-h-[200px]
      "
        >
            <div className="flex justify-between w-full border-b text-[10px] border-black dark:border-white">
                <div>19 points</div>
                <div className="rounded-full h-[5px] w-[5px] bg-green-500"></div>
            </div>
            <div className="flex gap-x-2 p-1">
                <PlayerCardImg />
                <PlayerDetail />
            </div>
        </div>
    );
}

function PlayerCardImg(  ) {
  const player = {
    name: "John Doe",
    grade: 2,
    gender: "male",
    points: 1200,
    created: new Date(),
};
    return (
        <Image
            src={`/images/images.jpeg-2.jpg`}
            alt={`${player.name}'s picture`}
            width={1000}
            height={1000}
            className="w-[80px] h-[80px] sm:w-[100px] sm:h-[100px]
      md:w-[120px] md:h-[120px] lg:w-[140px] lg:h-[140px] rounded-full"
        />
    );
}

function PlayerDetail() {
  const player = {
    name: "John Doe",
    grade: 2,
    gender: "male",
    points: 1200,
    created: new Date(),
    age: 22,
    role: "doctor"
};
    return (
        <div
            className={`${lusitana.className} p-1 overflow-auto max-h-[80px]
      sm:max-h-[100px] md:max-h-[120px] lg:max-h-[140px]
      flex flex-col justify-between tracking-widest
      text-nowrap text-xs border-l border-black dark:border-white w-full`}
        >
            <div>name: {player.name}</div>
            <div>gender: {player.gender}</div>
            <div>age: {player.age}</div>
            <div>role: {player.role}</div>
            <div className="text-pretty">
                cursed technique: no mercy{" "}
            </div>
            <div>
                colony no. 1: NG
            </div>
        </div>
    );
}

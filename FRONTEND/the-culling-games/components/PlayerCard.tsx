"use client";

import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { PlayerInfo } from "@/api/client";
import { KoganeImage } from "./KoganeImage";
import { Barcode } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { myPlayerOptions } from "@/api/client/@tanstack/react-query.gen";

export function PlayerCard() {
    const { data: player, error, isSuccess } = useQuery({
        ...myPlayerOptions(),
      }
    );

    if (!player) {
        return <NoPlayerCard />;
    }
    return <YesPlayerCard player={player} />;
}

function NoPlayerCard() {
    return (
        <Card className="p-0 shadow-sm bg-gray-200 dark:bg-gray-800 opacity-50 pointer-events-none overflow-hidden">
            <CardHeader className="p-1 max-h-min">
                <CardTitle className="flex justify-between">
                    <div className="flex">
                        <KoganeImage className="!w-8 !h-8 p-1 flex justify-center items-center" />
                        <p className="self-center font-serif font-extralight tracking-wide">
                            No Player Selected
                        </p>
                    </div>
                    <div>
                        <Badge variant="outline" className="text-xs max-h-max">
                            N/A
                        </Badge>
                    </div>
                </CardTitle>
                <CardDescription>
                    <div className="flex justify-center items-center gap-2">
                        <p className="text-pretty text-center">
                            No player data available
                        </p>
                    </div>
                </CardDescription>
            </CardHeader>
            <CardContent className="p-0">
                <div className="flex">
                    <div className="flex-1 flex flex-col text-sm px-2 gap-1">
                        <div className="flex gap-4">
                            ID Number{" "}
                            <p className="text-black font-semibold">N/A</p>
                        </div>
                        <div className="flex gap-12">
                            Name <p className="text-black font-semibold">N/A</p>
                        </div>
                        <div className="flex gap-8">
                            Birthday{" "}
                            <p className="text-black font-semibold">N/A</p>
                        </div>
                    </div>

                    <div className="relative mt-4">
                        <Avatar className="w-[100px] h-[100px] rounded-none">
                            <AvatarFallback className="w-[100px] h-[100px] rounded-none">
                                NP
                            </AvatarFallback>
                        </Avatar>
                        <div className="absolute -inset-3 border rounded-full h-8 w-8 flex justify-center items-center bg-black/90 text-white">
                            N/A
                        </div>
                    </div>
                </div>
            </CardContent>
            <CardFooter className="border-t p-1">
                <div className="w-full">
                    <div className="flex justify-center w-full">
                        <p className="text-[10px] font-light text-center">
                            {"NO PLAYER DATA AVAILABLE".toLocaleUpperCase()}
                        </p>
                    </div>
                    <div className="text-black flex justify-center">
                        <Barcode />
                        <Barcode />
                        <Barcode />
                        <Barcode />
                        <Barcode />
                        <Barcode />
                        <Barcode />
                        <Barcode />
                        <Barcode />
                        <Barcode />
                        <Barcode />
                    </div>
                </div>
            </CardFooter>
        </Card>
    );
}

interface PlayerCardProps {
    player: PlayerInfo;
}

function YesPlayerCard({ player }: PlayerCardProps) {
    return (
        <Card
            className="p-0 shadow-sm bg-gradient-to-tr from-[hsl(73,84%,60%)] to-emerald-500
            dark:bg-gradient-to-bl dark:from-indigo-600 dark:to-violet-900 dark:text-white overflow-hidden"
        >
            <CardHeader className="p-1 max-h-min">
                <CardTitle className="flex justify-between">
                    <div className="flex">
                        <KoganeImage className="!w-8 !h-8 p-1 flex justify-center items-center" />
                        <p className="self-center font-serif font-extralight tracking-wide">
                            The Culling Games
                        </p>
                    </div>

                    <div>
                        <Badge variant="outline" className="text-xs max-h-max">
                            {player?.role}
                        </Badge>
                    </div>
                </CardTitle>
                <CardDescription>
                    <div className="flex justify-center items-center gap-2">
                        <p className="text-pretty text-center">
                            This player? is currently
                        </p>
                        <Badge variant={"destructive"}>Dead</Badge>
                    </div>
                </CardDescription>
            </CardHeader>
            <CardContent className="p-0">
                <div className="flex">
                    <div className="flex-1 flex flex-col text-sm px-2 gap-1">
                        <div className="flex gap-4">
                            ID Number{" "}
                            <p className="text-black font-semibold">
                                {player?.id}
                            </p>
                        </div>
                        <div className="flex gap-12">
                            Name{" "}
                            <p className="text-black font-semibold">
                                {player?.name}
                            </p>
                        </div>
                        <div className="flex gap-8">
                            Birthday{" "}
                            <p className="text-black font-semibold">
                                {player?.age}
                            </p>
                        </div>
                    </div>

                    <div className="relative mt-4">
                        <Avatar className="w-[100px] h-[100px] rounded-none">
                            <AvatarImage
                                src="https://res.cloudinary.com/dd9xwf9wk/image/upload/v1731937774/website/profile_picture/website/profile_picture/enemchukwu_chukwuemeka_picture.jpg"
                                alt="@shadcn"
                            />
                            <AvatarFallback className="w-[100px] h-[100px] rounded-none">
                                EM
                            </AvatarFallback>
                        </Avatar>
                        <div className="absolute -inset-3 border rounded-full h-8 w-8 flex justify-center items-center bg-black/90 text-white ">
                            {player?.grade}
                        </div>
                    </div>
                </div>
            </CardContent>

            <CardFooter className="border-t p-1">
                <div className="w-full">
                    <div className="flex justify-center w-full">
                        <p className="text-[10px] font-light text-center">
                            {"The Above Proves this individual is a player? in the culling games".toLocaleUpperCase()}
                        </p>
                    </div>
                    <div className="text-black flex justify-center">
                        <Barcode />
                        <Barcode />
                        <Barcode />
                        <Barcode />
                        <Barcode />
                        <Barcode />
                        <Barcode />
                        <Barcode />
                        <Barcode />
                        <Barcode />
                        <Barcode />
                    </div>
                </div>
            </CardFooter>
        </Card>
    );
}

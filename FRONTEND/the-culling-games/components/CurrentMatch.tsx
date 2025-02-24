"use client";

import { MatchInfo } from "@/api/client";
import {
    Card,
    CardContent,
    CardFooter,
    CardHeader,
} from "@/components/ui/card";
import { useLatestMatchQuery } from "@/lib/custom-hooks/match-queries";
import React from "react";

export function LatestMatch() {
    const accessToken = localStorage.getItem("access_token");

    const { data: match, error } = useLatestMatchQuery(accessToken);
    console.log(accessToken)
    if (!match) {
        console.log(error)
        return <NoMatchCard />;
    }
    return <MatchCard match={match} />;
}

type MatchCardProps = {
    match: MatchInfo;
};

function MatchCard({ match }: MatchCardProps) {
    const timeLeft = () => {
        const endTime = new Date(match.end).getTime();
        const now = new Date().getTime();
        const difference = endTime - now;

        if (difference > 0) {
            return Math.floor(difference / 1000); // return seconds left
        }
        return 0;
    };

    return (
        <Card className="flex flex-col justify-between max-h-max max-w-sm bg-gradient-to-bl from-yellow-500 to-red-500 text-black">
            <CardHeader className="flex flex-row justify-between items-center p-2 space-y-0">
                <div className="rounded-full px-2 py-1 bg-green-600 text-white text-xs">
                    {`Colony ${match.colony.id}: ${match.colony.country}`}
                </div>
                <div className="rounded-full bg-black px-2 py-1 text-white text-xs">
                    {timeLeft() > 0 ? `Time left: ${timeLeft()}s` : "Ended"}
                </div>
            </CardHeader>
            <CardContent className="p-4">
                <div className="flex w-full flex-nowrap justify-around items-center gap-5 font-bold mb-4">
                    {match.players.map((player, ind) => (
                        <React.Fragment key={player.id}>
                            <div className="flex justify-between">
                                <span className="flex-1 text-center truncate">
                                    {player.name}
                                </span>
                            </div>
                            {ind !== match.players.length - 1 && (
                                <span className="self-center font-extralight text-sm">
                                    VS
                                </span>
                            )}
                        </React.Fragment>
                    ))}
                </div>
            </CardContent>

            <CardFooter className="flex justify-between text-xs p-2">
                {match.players.map((player, ind) => (
                    <React.Fragment key={player.id}>
                        <div>
                            <span key={player.id} className="text-red-950">
                                {`points: ${player.points}`}
                            </span>
                        </div>
                        {ind !== match.players.length - 1 && (
                            <span key={player.id}>|</span>
                        )}
                    </React.Fragment>
                ))}
            </CardFooter>
        </Card>
    );
}

function NoMatchCard() {
    return (
        <Card className="flex flex-col justify-between max-h-max max-w-md bg-gradient-to-bl from-gray-700 to-gray-900 text-white">
            <CardHeader className="flex flex-row justify-between items-center p-2 space-y-0">
                <div className="rounded-full px-2 py-1 bg-blue-600 text-white text-xs">
                    No Latest Match
                </div>
            </CardHeader>
            <CardContent className="p-4">
                <p>There is currently no match available.</p>
            </CardContent>
            <CardFooter className="flex justify-center text-xs p-2">
                <span>Please check back later.</span>
            </CardFooter>
        </Card>
    );
}

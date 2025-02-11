import { MatchInfo, Gender } from "@/api/client";
import {
    Card,
    CardContent,
    CardFooter,
    CardHeader,
} from "@/components/ui/card";

function MatchCard() {
    const match: MatchInfo = {
        id: 1,
        begin: new Date(),
        end: new Date(),
        part: 1,
        winner: null,
        players: [
            {
                id: 2,
                name: "Crusader",
                age: undefined,
                role: undefined,
                gender: Gender.MALE,
                created: new Date(),
                grade: 4,
                points: 2.4,
            },
            {
                id: 1,
                name: "SparrowKing",
                age: undefined,
                role: undefined,
                gender: Gender.MALE,
                created: new Date(),
                grade: 4,
                points: 2.4,
            },
        ],
        colony: {
            id: 1,
            country: "AD",
        },
    };

    return (
        <div
            className={`flex flex-col rounded-xl px-4 py-1 lg:w-[50%]
			bg-gradient-to-bl from-yellow-500 to-red-500 gap-2
			min-h-[150px] max-h-[300px] justify-evenly sm:justify-between`}
        >
            <div className="flex self-center w-full justify-between gap-2 text-xs text-nowrap">
                <div className="rounded-full px-1 bg-green-600">{`Colony ${match.colony.id}: ${match.colony.country}`}</div>
                <div className="rounded-full bg-black px-1 text-white">
                    {new Date().getSeconds() -
                        new Date(match.end).getSeconds() >
                    0
                        ? `Time left: ${
                              new Date().getSeconds() -
                              new Date(match.end).getSeconds()
                          }`
                        : "Ended"}
                </div>
            </div>
            <div className={`p-2 gap-y-6 flex flex-col items-center`}>
                <div className="flex justify-around sm:justify-evenly gap-5 px-2 text-black font-bold">
                    <span className="text-center">{match.players[0].name}</span>{" "}
                    <span className="!font-extralight h-fit self-center text-sm">
                        VS
                    </span>{" "}
                    <span className="text-center">{match.players[1].name}</span>
                </div>
                <div className="flex justify-between text-[12px] w-full">
                    <span
                        className={`!text-red-950`}
                    >{`points: ${match.players[0].points}`}</span>{" "}
                    <span>|</span>{" "}
                    <span
                        className={`text-green-950`}
                    >{`points: ${match.players[1].points}`}</span>
                </div>
            </div>
        </div>
    );
}

export function CurrentMatch() {
    const match: MatchInfo = {
        id: 1,
        begin: new Date(),
        end: new Date(),
        part: 1,
        winner: null,
        players: [
            {
                id: 2,
                name: "Crusader",
                age: undefined,
                role: undefined,
                gender: Gender.MALE,
                created: new Date(),
                grade: 4,
                points: 2.4,
            },
            {
                id: 1,
                name: "SparrowKing",
                age: undefined,
                role: undefined,
                gender: Gender.MALE,
                created: new Date(),
                grade: 4,
                points: 2.4,
            },
        ],
        colony: {
            id: 1,
            country: "AD",
        },
    };

    const timeLeft = () => {
        const endTime = match.end.getTime();
        const now = new Date().getTime();
        const difference = endTime - now;

        if (difference > 0) {
            return Math.floor(difference / 1000); // return seconds left
        }
        return 0;
    };

    return (
        <Card className="w-full max-w-md bg-gradient-to-bl from-yellow-500 to-red-500 text-black">
            <CardHeader className="flex flex-row justify-between items-center p-2 space-y-0">
                <div className="rounded-full px-2 py-1 bg-green-600 text-white text-xs">
                    {`Colony ${match.colony.id}: ${match.colony.country}`}
                </div>
                <div className="rounded-full bg-black px-2 py-1 text-white text-xs">
                    {timeLeft() > 0 ? `Time left: ${timeLeft()}s` : "Ended"}
                </div>
            </CardHeader>
            <CardContent className="p-4">
                <div className="flex justify-around items-center gap-5 font-bold mb-4">
                    <span className="text-center">{match.players[0].name}</span>
                    <span className="font-extralight text-sm">VS</span>
                    <span className="text-center">{match.players[1].name}</span>
                </div>
            </CardContent>
            <CardFooter className="flex justify-between text-xs p-2">
                <span className="text-red-950">{`points: ${match.players[0].points.toFixed(
                    1
                )}`}</span>
                <span>|</span>
                <span className="text-green-950">{`points: ${match.players[1].points.toFixed(
                    1
                )}`}</span>
            </CardFooter>
        </Card>
    );
}

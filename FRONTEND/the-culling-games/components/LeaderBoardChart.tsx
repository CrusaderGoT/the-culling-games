"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";

// Define a simple Player interface for the leaderboard data
interface Player {
    id: number;
    name: string;
    points: number;
    wins: number;
    matchesPlayed: number;
}

// Sample data – in a real app, this could be fetched from an API or database
const players: Player[] = [
    { id: 1, name: "Player One", points: 1500, wins: 10, matchesPlayed: 15 },
    { id: 2, name: "Player Two", points: 1300, wins: 8, matchesPlayed: 12 },
    { id: 3, name: "Player Three", points: 1200, wins: 7, matchesPlayed: 10 },
    { id: 4, name: "Player Four", points: 1100, wins: 6, matchesPlayed: 11 },
];

export function LeaderboardChart() {
    return (
        <Card>
            <CardHeader className="flex justify-between items-center">
                <CardTitle className="text-xl font-bold">Leaderboard</CardTitle>
                <Button>Refresh</Button>
            </CardHeader>
            <CardContent>
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>Rank</TableHead>
                            <TableHead>Name</TableHead>
                            <TableHead>Points</TableHead>
                            <TableHead>Wins</TableHead>
                            <TableHead>Matches</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {players.map((player, index) => (
                            <TableRow key={player.id}>
                                <TableCell>{index + 1}</TableCell>
                                <TableCell>{player.name}</TableCell>
                                <TableCell>{player.points}</TableCell>
                                <TableCell>{player.wins}</TableCell>
                                <TableCell>{player.matchesPlayed}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </CardContent>
        </Card>
    );
}

function Leaderboard() {
    return (
        <canvas
            className="rounded-xl bg-stone-700 text-white
		w-full max-h-[31%] lg:h-[50%] md:w-[200%] lg:w-full
		invert dark:invert-0"
        ></canvas>
    );
}

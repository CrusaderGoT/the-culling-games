"use client"

import { LeaderboardChart } from "@/components/Chart";
import { ColonyStatus } from "@/components/ColonyCard";
import { ColonyPlayerGradeChart } from "@/components/ColonyPlayersGradeChart";
import { LatestMatch } from "@/components/CurrentMatch";
import { PlayerCard } from "@/components/PlayerCard";
import { CommentSection } from "@/components/SocialBoard";

export default function Dashboard() {
    return (
        <div className="flex flex-col justify-between gap-3 p-4 container min-h-screen">
            <div className="flex gap-2 flex-1">
                <div className="w-2/3 flex flex-col gap-2 justify-between">
                    <div className="flex flex-col md:flex-row gap-2 flex-1 justify-between">
                        <div className="flex flex-col gap-1 flex-1">
                            <div>
                                <LatestMatch />
                            </div>
                            <div>
                                <PlayerCard />
                            </div>
                        </div>
                        <div>
                            <ColonyPlayerGradeChart />
                        </div>
                    </div>

                    <div>
                        <ColonyStatus />
                    </div>
                </div>

                <div className="w-1/3">
                    <CommentSection />
                </div>
            </div>

            <div className="">
                <LeaderboardChart />
            </div>
        </div>
    );
}

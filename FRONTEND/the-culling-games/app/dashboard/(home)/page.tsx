import { CurrentMatch } from "./CurrentMatch";
import { PlayerCard } from "./PlayerCard";

function ColonyCard() {
    // each colony has 10 players 100%
    // make a logic that calculates where to place the red line depending on how many players are left
    return (
        <div
            className={`rounded-xl overflow-hidden border border-green-800 flex justify-between h-fit text-nowrap`}
        >
            <div
                className={`bg-gradient-to-r w-[30%] flex items-center justify-center overflow-clip from-[hsla(0,100%,50%,100%)] h-full text-center text-xs`}
            >
                {" "}
                3 dead
            </div>
            <div
                className={`bg-gradient-to-l w-[70%] flex items-center justify-center overflow-clip text-xs from-[hsla(120,100%,50%,100%)] h-full`}
            >
                7 alive
            </div>
        </div>
    );
}

function Chart() {
    return (
        <canvas
            className="rounded-xl bg-stone-700 text-white
		w-full max-h-[31%] lg:h-[50%] md:w-[200%] lg:w-full
		invert dark:invert-0"
        ></canvas>
    );
}

function SocialBoard() {
    return (
        <div className="flex flex-col h-full w-full rounded-xl px-3 py-1 border border-black dark:border-white border-dashed">
            <h2 className="font-bold text-lg self-center underline underline-offset-2">
                Social Media Comments
            </h2>
            <div className="h-full my-2">vvv</div>
        </div>
    );
}

export default function Dashboard() {
    return (
        <div className="flex flex-col sm:flex-row justify-between h-full w-full p-3 gap-5">
            <section
                className="h-full sm:w-[50%] lg:w-[75%]
			lg:flex-col-reverse flex flex-col gap-5 lg:justify-around"
            >
                <div className="flex flex-col lg:flex-row gap-3 invert dark:invert-0">
                    <CurrentMatch />
                    <PlayerCard />
                </div>

                <div className="w-full">
                    <ColonyCard />
                </div>

                <Chart />
            </section>

            <section className="h-[500px] sm:h-auto sm:w-[50%] lg:w-[25%] md:h-[61%] lg:h-auto">
                <SocialBoard />
            </section>
        </div>
    );
}

export function ColonyCard() {
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

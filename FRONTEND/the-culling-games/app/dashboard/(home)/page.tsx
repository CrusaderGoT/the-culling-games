function CurrentMatch() {
	return (
		<div className={
			`flex flex-col rounded-xl px-4 py-1 lg:w-[50%]
			bg-gradient-to-bl from-yellow-500 to-red-500 gap-2
			min-h-[150px] max-h-[300px] justify-evenly sm:justify-between`
		}>
			<div className="flex self-center w-full justify-between gap-2 text-xs text-nowrap">
				<div className="rounded-full px-1 bg-green-600">Colony 3: Kenya</div>
				<div className="rounded-full bg-black px-1 text-white">time left: 12:09</div>
			</div>
			<div className={`p-2 gap-y-6 flex flex-col items-center`}>
				<div className="flex justify-around sm:justify-evenly gap-5 px-2 text-black font-bold">
					<span className="text-center">Sparrow King</span> <span className="!font-extralight h-fit self-center text-sm">VS</span> <span className="text-center">Boulder Man</span>
				</div>
				<div className="flex justify-between text-[12px] w-full">
					<span className={`!text-red-950`}>points: 40</span> <span>|</span> <span className={`text-green-950`}>points: 50</span>
				</div>
			</div>
		</div>
	);
}

function PlayerCard() {
	// get player from api
	return (
		<div className="flex flex-col px-3 py-1 rounded-xl gap-9 lg:w-[50%]
							bg-gradient-radial from-pink-600 from-50% to-violet-700"
		>
			<div className="flex justify-between gap-3 text-nowrap">
				<span>points</span>
				<span>grade</span>
			</div>

			<div className="self-center">
				<span>Player Name</span>
			</div>

			<div className="flex justify-between gap-3 text-nowrap">
				<span>wins</span>
				<span>stats</span>
			</div>
		</div>
	);
}

function ColonyCard() {
	// each colony has 10 players 100%
	// make a logic that calculates where to place the red line depending on how many players are left
	return (
		<div className={`rounded-xl overflow-hidden border border-green-800 flex justify-between h-fit text-nowrap`}>
			<div className={`bg-gradient-to-r w-[30%] flex items-center justify-center overflow-clip from-[hsla(0,100%,50%,100%)] h-full text-center text-xs`}> 3 dead</div>
			<div className={`bg-gradient-to-l w-[70%] flex items-center justify-center overflow-clip text-xs from-[hsla(120,100%,50%,100%)] h-full`}>7 alive</div>
		</div>
	);
}

function Chart() {
	return (
		<canvas className="rounded-xl bg-stone-700 text-white
		w-full max-h-[31%] lg:h-[50%] md:w-[200%] lg:w-full
		invert dark:invert-0"></canvas>		
	);
}

function SocialBoard() {
	return (
		<div className="flex flex-col h-full w-full rounded-xl px-3 py-1 border border-black dark:border-white border-dashed">
			<h2 className="font-bold text-lg self-center underline underline-offset-2">Social Media Comments</h2>
			<div className="h-full my-2">vvv</div>
		</div>
	);
}




export default function Dashboard() {
	return (
		<div className="flex flex-col sm:flex-row justify-between h-full w-full p-3 gap-5">
			
			<section className="h-full sm:w-[50%] lg:w-[75%]
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
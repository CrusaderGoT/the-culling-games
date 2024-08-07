function PlayerCard() {
	// get player from api
	return (
		<section className="flex flex-col md:w-[50%] md:h-fit px-3 py-1 rounded-3xl gap-9 bg-gradient-radial from-slate-600 to-slate-600 invert dark:invert-0">
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
		</section>
	)
	
}

function CurrentMatch() {
	return (
		<section className="bg-red-400 rounded-3xl px-3 py-1 md:w-[50%] md:h-[100%]">
			vjvjjvv
		</section>
	)
}

function SocialBoard() {
	return (
		<section className="bg-red-400 rounded-3xl px-3 py-1 md:w-[50%] md:h-[100%]">
			vjvjjvv
		</section>
	)
}




export default function Dashboard() {
	return (
		<div className="w-full p-5 flex flex-col md:flex-row gap-5">
			<CurrentMatch />
			<PlayerCard />
			<SocialBoard />

		</div>
	)
}
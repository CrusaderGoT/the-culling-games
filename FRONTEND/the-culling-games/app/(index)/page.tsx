"use server"
import index from "./index.module.css"



export default async function Home() {
  return (
    <main className="w-full h-screen bg-gradient-radial from-slate-400 to-slate-900 font-mono text-sm flex items-center justify-center">
      <ColonyCircle />
    </main>
  );
}

function ColonyCircle() {
  return (
    <div className={
      `${index.colonyCircle} p-5 overflow-hidden w-[90vw]
      h-[90vw] md:w-[70vw] md:h-[70vw] lg:w-[90vh] lg:h-[90vh]
      max-w-[99%] max-h-[99%] bg-black bg-opacity-90
      hover:bg-opacity-80 rounded-full cursor-default`
      }>
      <CircleContent />
    </div>
  );
}

function CircleContent() {
  return (
    <div className="relative rounded-full flex flex-col items-center justify-center w-full h-full">
      <h2 className={
        `${index.colonyText} font-semibold
        sm:font-bold lg:font-extrabold tracking-[10px]
        md:tracking-[20px] lg:tracking-[30px]
        text-lg sm:text-2xl md:text-3xl
        absolute top-1/2 translate-y-[-50%] z-[2]`
      }>COLONY
      </h2>
      <p className={
        `${index.colonyWarn} absolute bottom-[-17px] sm:bottom-0 w-full text-[10px]
        leading-3 sm:text-xs text-pretty px-[30%] sm:px-[5%]
        text-center m-2`
        }>a dangerous game is going on inside &#x1F6C8;
      </p>
      <button type="button" className={
        `${index.colonyBtn} opacity-0 absolute bottom-[25%]
        h-[12px] w-[32px] sm:h-[20px] sm:w-[50px] rounded-full
        text-[9px] sm:text-[12px] md:text-base font-semibold
        tracking-wider flex items-center justify-center
        bg-gradient-conic from-slate-600 via-slate-900 to-black`
        }>YES
      </button>
    </div> 
  )
}

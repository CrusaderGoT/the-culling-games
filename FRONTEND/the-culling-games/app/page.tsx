import Image from "next/image";
import styles from "./page.module.css";
import { courier } from "./layout";

export default function Home() {
  return (
    <main className={`
      min-h-screen min-w-full
      bg-transparent p-[20px]
      `}>
      <CircleContainer
        circle={<ColonyCircle
          content={<CircleContent />}
        />}
      />
    </main>
  );
}

function CircleContainer({circle}) {
  return (
    <div
      className={`
        relative flex
        min-w-[100px] min-h-[100px] w-[300px] h-[300px]
        sm:min-w-[640px] sm:min-h-[640px]
        lg:max-w-[1024px] lg:max-h-[1024px]
      `}
    >
      <Image
        className={`
          absolute
          sm:min-w-[640px] sm:min-h-[640px]
          lg:max-w-[1024px] lg:max-h-[1024px]
        `}
        src='/skyline.jpg'
        alt='kfk'
        width={300}
        height={300}
      ></Image>
      {circle}
    </div>
  )
}

function ColonyCircle({content}) {
  return (
    <div
      className={`
        relative
        min-w-[100px] min-h-[100px] w-[300px] h-[300px]
        sm:min-w-[640px] sm:min-h-[640px]
        lg:max-w-[1024px] lg:max-h-[1024px]
        border rounded-full border-black
        bg-black hover:opacity-90 overflow-autfo text-white
        flex justify-center p-3
        tracking-widest sm:tracking-[1rem] md:tracking-[2rem]

      `}
    >
      {content}
    </div>
  )
}

function CircleContent() {
  return (
    <div className={`
      w-fit h-fit flex flex-col border border-black
      m-[5%] place-self-center hover:place-self-start
      ${courier.className}
    `}>
      <h2>Colony</h2>
    </div>
  );
}


// for defining the components of the signup page -> down to top.
"use client"

import { roboto_mono, lusitana } from "../../fonts";
import Image from "next/image";
import { UserForm } from "../UserForm";

function Description() {
    return (
        <div className="mb-1 sm:m-5 w-full flex flex-1 relative overflow-hidden rounded-xl">
            <Image
                src="/images/Kogane_showing_player_data.png"
                alt="info-kogane.jpg"
                height={663}
                width={519}
                className="absolute h-full w-full"
            />
            <p className={`${lusitana.className} z-10 w-full sm:h-full h-[200px] p-2 bg-black/80 text-white text-sm sm:text-base overflow-y-auto`}>
                Explaination of the games Explaination of the games Explaination of the games
            </p>
        </div>
    );
}

export default function SignUpPage() {
    return (
            <div className={`${roboto_mono.className} p-5 rounded-md shadow-lg dark:shadow-white dark:shadow-md m-10`}>
                <h3 className={`font-extrabold text-2xl mb-3`}>Register to Play</h3>
                <div className="flex flex-col-reverse sm:flex-row justify-between">
                    <UserForm />
                    <Description />
                </div>
            </div>
    );
}
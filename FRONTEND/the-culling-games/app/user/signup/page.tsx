// for defining the components of the signup page -> down to top.
"use client";

import Image from "next/image";
import { CreateUserForm } from "./CreateUserForm";

function Description() {
    return (
        <div className="flex contain-content rounded-xl min-h-96 max-h-[80%] max-w-[90%] mx-auto relative">
            <Image
                src="/images/Kogane_showing_player_data.png"
                alt="info-kogane.jpg"
                height={663}
                width={519}
                className="absolute h-full w-full"
            />
            <p className="z-10 bg-black/70 sticky p-2 text-white text-base overflow-y-auto">
                Explaination of the games Explaination of the games Explaination
                of the games
            </p>
        </div>
    );
}

export default function SignUpPage() {
    return (
        <div className="sm:m-5 m-3 flex flex-col">
            <h3 className="font-bold text-xl mb-3 self-center">Register to Play</h3>
            <div className="flex flex-col sm:flex-row gap-3 self-center">
                <Description />
                <CreateUserForm />
            </div>
        </div>
    );
}

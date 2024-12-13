import { useActionState } from "react";
// for defining the components of the signup page -> down to top.
"use client"
import { createUser } from "../api/routes";
import { roboto_mono, lusitana } from "../fonts";
import Image from "next/image";
import { useFormStatus } from "react-dom";


export function UsernameInput() {
    return (
        <>
            <label htmlFor="usernameId">
                Username
                <input required className="rounded p-1 w-full" type="text" name="username" id="usernameId" title="username" />
            </label>
            
        </>    
    );
}

export function EmailInput() {
    return (
        <>
            <label htmlFor="emailId">
                Email
                <input required className="rounded p-1 w-full" type="email" name="email" id="emailId" title="email" />
            </label>
            
        </>    
    );
}

function CountryInput() {
    return (
        <>
            <label htmlFor="countryId">Country</label>
            <select className="rounded p-1 w-full" name="country" id="countryId">
            </select>
        </>    
    );
}

export function PasswordInput() {
    return (
        <>
            <label htmlFor="passwordId">
                Password
                <input required className="rounded p-1 w-full" type="password" name="password" id="passwordId" title="password" />
            </label>
            
        </>    
    );
}

function ConfirmPasswordInput() {
    return (
        <>
            <label htmlFor="confirmPasswordId">
                Confirm Password
                <input required className="rounded p-1 w-full" type="password" name="confirm_password" id="confirmPasswordId" title="confirm password" />
            </label>
            
        </>    
    );
}

export function SubmitButton({title}: {title: string}) {
    const { pending } = useFormStatus()
    return (
        <button type="submit" disabled={pending} className="bg-yellow-400 hover:bg-yellow-300 text-sm active:bg-yellow-200 disabled:opacity-20 h-fit w-fit mt-3 p-1 rounded-md">{title}</button>
    );
}

function FormInput() {
    const initialState = { //message to show if unsuccesfull
        detail: ''
    }
    const [state, formAction] = useActionState(createUser, initialState)
    return (
        <> 
        <form action={formAction} className="flex flex-col gap-2 sm:w-[50%] lg:w-[25%]">
                <p className="text-red-400 font-bold">{state?.detail}</p>
                <UsernameInput />
                <EmailInput />
                <CountryInput />
                <PasswordInput />
                <ConfirmPasswordInput />
                <SubmitButton title="Register" />
            </form>	    
        </>
                 
    );
}

function Description() {
    return (
        <div className="mb-1 sm:m-5 sm:w-[50%] lg:w-[75%] flex relative overflow-hidden rounded-t-xl rounded-b-xl">
            <Image
                src="/images/Kogane_showing_player_data.png"
                alt="info-kogane.jpg"
                height={663}
                width={519}
                className="absolute h-full w-full"
            />
            <p className={`${lusitana.className} z-10 w-full sm:h-full h-[200px] p-2 bg-black opacity-70 text-white text-sm sm:text-base overflow-y-auto`}>
                Explaination of the games Explaination of the games Explaination of the games
            </p>
        </div>
    );
}

export default function SignupPage() {
    return (
        <main className="p-10 pt-[100px] min-w-[250px] mx-auto my-auto min-h-screen w-screen">
            <div className={`dark:text-black ${roboto_mono.className} p-10 sm:pr-0 rounded-md bg-gradient-to-br from-slate-700 to-slate-300 shadow-lg dark:shadow-white dark:shadow-md`}>
                <h3 className={`font-extrabold text-2xl mb-3`}>Register to Play</h3>
                <div className="flex flex-col-reverse sm:flex-row justify-between">
                    <FormInput />
                    <Description />
                </div>
            </div>
        </main>
    );
}
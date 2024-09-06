// defines the login page
"use client"
import { useFormState } from "react-dom";
import { UsernameInput, PasswordInput, SubmitButton } from "../signup/page"
import { login } from "./api/routes";

function LoginForm() {
    const initialState = { //message to show if unsuccesfull
        detail: ''
    }
    const [state, formAction] = useFormState(login, initialState)
    return (
        <form action={formAction} className="!text-black rounded-lg mx-auto bg-gradient-to-b from-slate-300 via-gray-400 to-slate-600 p-3 flex flex-col gap-4 sm:w-[50%]">
            <p className="text-2xl font-extralight">Login</p>
            <p className="text-red-400 font-bold">{state?.detail}</p>
            <UsernameInput />
            <PasswordInput />
            <SubmitButton title="Log In" />
        </form>

    )
}

export default function LoginPage() {
    return (
        <main className="p-10 pt-[100px] invert min-w-[250px] min-h-screen w-screen">
          <LoginForm />
        </main>
    );
}


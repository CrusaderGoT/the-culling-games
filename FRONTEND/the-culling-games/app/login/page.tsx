// defines the login page
import { UsernameInput, PasswordInput, SubmitButton } from "../signup/page"
import { login } from "./api/routes";

function LoginForm() {
    return (
        <form action={login} className="rounded-lg bg-gradient-to-b from-slate-300 via-gray-400 to-slate-600 p-3 flex flex-col gap-4 sm:w-[50%] mx-auto">
            <p className="text-2xl font-extralight">Login</p>
            <UsernameInput />
            <PasswordInput />
            <SubmitButton title="Log In" />
        </form>

    )
}

export default function LoginPage() {
    return (
        <main className="p-10 mx-auto my-auto min-w-[300px] min-h-screen w-screen]">
          <LoginForm />
        </main>
    );
}


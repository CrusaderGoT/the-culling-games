"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";

import { Form } from "@/components/ui/form";

import { InputWithLabel } from "@/components/inputs/InputWithLabel";
import { SelectWithLabel } from "@/components/inputs/SelectWithLabel";
import { LinkButton } from "@/components/LinkButton";
import { Button } from "@/components/ui/button";
import { LoaderCircle, LogInIcon, UserPlus2Icon } from "lucide-react";

import { Country, CreateUser } from "@/api/client";
import { zCreateUser } from "@/api/client/zod.gen";
import { DisplayResponseMessage } from "@/components/DisplayServerResponse";
import { COUNTRIES } from "@/constants/COUNTRIES";
import {
    useLoginMutation,
    useSignUpMutation,
} from "@/lib/custom-hooks/user-mutations";

export function CreateUserForm() {
    const router = useRouter();

    router.prefetch("/dashboard");
    router.prefetch("/user/login");

    const defaultValues: CreateUser = {
        username: "",
        email: "",
        country: Country.AD,
        password: "",
        confirm_password: "",
    };

    const form = useForm<CreateUser>({
        resolver: zodResolver(zCreateUser),
        defaultValues,
    });

    // Define the signup mutation with its success/error side effects.
    const signupMutation = useSignUpMutation();

    // Define the login mutation with its side effects.
    const loginMutation = useLoginMutation();

    // Use async/await to chain the signup and login flows.
    async function onSubmit(data: CreateUser) {
        try {
            // Wait for the signup to complete.
            await signupMutation.mutateAsync({ body: data });

            // Then, log in the user.
            await loginMutation.mutateAsync({
                body: { username: data.username, password: data.password },
            });
        } catch (error) {
            // Errors are already handled by each mutation's onError callback.
            alert("Signup/Login error");
        }
    }

    // booleans for display a loading indicator, or diasbling buttons.
    const isSigningUp = signupMutation.isPending;
    const isLoggingIn = loginMutation.isPending;

    const signUpSuccess = signupMutation.isSuccess;
    const loginSuccess = loginMutation.isSuccess;

    const signUpError = signupMutation.error;

    return (
        <div className="sm:px-8 p-4 min-w-[50%]">
            {(isSigningUp || isLoggingIn) && (
                <div className="w-full max-w-xs flex justify-center items-center text-xs font-semibold">
                    <LoaderCircle className="animate-spin max-h-full ml-2 text-lime-300 w-[12px]" />
                    {isSigningUp && (
                        <span className="text-blue-400">
                            Creating your User...
                        </span>
                    )}
                    {isLoggingIn && (
                        <span className="text-green-500">
                            User Created Successfully, Logging in the user...
                        </span>
                    )}
                    {loginSuccess && (
                        <span className="text-yellow-500">
                            Logged in successfully, redirecting to dashboard...
                        </span>
                    )}
                </div>
            )}
            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)}>
                    <div className="flex flex-col gap-6">
                        <div className="flex flex-col gap-4">
                            <InputWithLabel<CreateUser>
                                fieldTitle="Username"
                                nameInSchema="username"
                                placeholder="your username is not the same as player name"
                            />

                            <InputWithLabel<CreateUser>
                                fieldTitle="Email"
                                nameInSchema="email"
                                type="email"
                                autoComplete="false"
                                placeholder="myemail@example.com"
                            />

                            <SelectWithLabel<CreateUser>
                                data={COUNTRIES}
                                fieldTitle="Country"
                                nameInSchema="country"
                            />

                            <InputWithLabel<CreateUser>
                                fieldTitle="Password"
                                nameInSchema="password"
                                type="password"
                                autoComplete="off"
                                aria-autocomplete="none"
                            />

                            <InputWithLabel<CreateUser>
                                fieldTitle="Confirm Password"
                                nameInSchema="confirm_password"
                                type="password"
                                autoComplete="off"
                                aria-autocomplete="none"
                            />

                            {signUpError && (
                                <DisplayResponseMessage error={signUpError} />
                            )}
                        </div>

                        <div className="flex flex-col items-start gap-3 sm:flex-row w-max">
                            <Button
                                disabled={
                                    isSigningUp || isLoggingIn || signUpSuccess
                                }
                                type="submit"
                                className="flex text-center gap-1 max-w-max max-h-max"
                                title="Create Account"
                            >
                                Create Account
                                <div className="hidden sm:block">
                                    <UserPlus2Icon />
                                </div>
                            </Button>

                            <div className="sm:self-center font-semibold">
                                <p>or</p>
                            </div>

                            <LinkButton
                                disabled={
                                    isSigningUp || isLoggingIn || loginSuccess
                                }
                                href="/user/login"
                                label="Login"
                                icon={LogInIcon}
                            />
                        </div>
                    </div>
                </form>
            </Form>
        </div>
    );
}

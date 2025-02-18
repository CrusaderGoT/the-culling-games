"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";
import { toast } from "sonner";
import { useRouter } from "next/navigation";

import { Form } from "@/components/ui/form";

import { SelectWithLabel } from "@/components/inputs/SelectWithLabel";
import { InputWithLabel } from "@/components/inputs/InputWithLabel";
import { Button } from "@/components/ui/button";
import { LinkButton } from "@/components/LinkButton";
import { LogInIcon, UserPlus2Icon, LoaderCircle } from "lucide-react";

import { CreateUser, Country } from "@/api/client";
import { zCreateUser } from "@/api/client/zod.gen";
import {
    createTokenMutation,
    createUserMutation,
} from "@/api/client/@tanstack/react-query.gen";
import { COUNTRIES } from "@/constants/COUNTRIES";
import { DisplayResponseMessage } from "@/components/DisplayServerResponse";

export function CreateUserForm() {
    const router = useRouter();

    router.prefetch("/dashboard");
    router.prefetch("/user/login");

    const defaultValues: CreateUser = {
        username: "Zanib",
        email: "mcdonald@gmail.com",
        country: Country.AD,
        password: "SpparrowKing1234@@",
        confirm_password: "SpparrowKing1234@@",
    };

    const form = useForm<CreateUser>({
        resolver: zodResolver(zCreateUser),
        defaultValues,
    });

    // Define the signup mutation with its success/error side effects.
    const signupMutation = useMutation({
        ...createUserMutation(),
        onError: (error) => {
            if (error.detail) {
                toast(
                    `${
                        typeof error?.detail === "string"
                            ? error.detail
                            : "A sign up error occurred"
                    }`
                );
            } else {
                toast("A sign up error occurred");
            }
        },
        onSuccess: (data) => {
            toast(`User '${data.username}' created successfully`);
        },
        retry: 3,
    });

    // Define the login mutation with its side effects.
    const loginMutation = useMutation({
        ...createTokenMutation(),
        onError: (error) => {
            if (error.detail) {
                toast(
                    `${
                        typeof error?.detail === "string"
                            ? error.detail
                            : "A log in error occurred"
                    }`
                );
            }
        },
        onSuccess: (data) => {
            localStorage.setItem("access_token", data.access_token);
            router.push("/dashboard");
        },
        retry: 3,
    });

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
            console.error("Signup/Login error", error);
        }
    }

    // Optionally, display a loading indicator.
    const isSigningUp = signupMutation.status === "pending";
    const isLoggingIn = loginMutation.status === "pending";

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
                            User Created Successfully: Logging in the user...
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
                            />

                            <InputWithLabel<CreateUser>
                                fieldTitle="Email"
                                nameInSchema="email"
                                type="email"
                                autoComplete="false"
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
                                disabled={isSigningUp || isLoggingIn}
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
                                disabled={isSigningUp || isLoggingIn}
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

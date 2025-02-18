"use client";

import { SelectWithLabel } from "@/components/inputs/SelectWithLabel";
import { type CreateUser, Country } from "@/api/client";
import { zCreateUser } from "@/api/client/zod.gen";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Form } from "@/components/ui/form";
import { InputWithLabel } from "@/components/inputs/InputWithLabel";
import { Button } from "@/components/ui/button";
import { LinkButton } from "@/components/LinkButton";
import { LogInIcon, UserPlus2Icon } from "lucide-react";
import { COUNTRIES } from "@/constants/COUNTRIES";
import { useMutation } from "@tanstack/react-query";
import {
    createTokenMutation,
    createUserMutation,
} from "@/api/client/@tanstack/react-query.gen";
import { toast } from "sonner";
import { useRouter } from "next/navigation";

export function CreateUserForm() {
    const router = useRouter();

    const defaultValues: CreateUser = {
        username: "Zanib",
        email: "mcdonald@gmail.com",
        country: Country.AD,
        password: "SpparrowKing1234@@",
        confirm_password: "SpparrowKing1234@@",
    };

    const form = useForm<CreateUser>({
        resolver: zodResolver(zCreateUser),
        defaultValues: defaultValues,
    });

    const {
        isPending: isLoggingIn,
        isSuccess: isLoginSuccess,
        isError: isLoginError,
        mutate: login,
    } = useMutation({
        ...createTokenMutation(),
        onError: (error) => {
            if (error.detail) {
                toast(`${error.detail}`);
            } else {
                toast("A login error occured");
            }
        },
        onSuccess: (data) => {
            // save token to cookie; did not work
            const tokenString = data.access_token;
            localStorage.setItem("access_token", tokenString);
            // invalidate prev user; refetch user query keys
        },
    });

    const {
        mutate: signup,
        isPending: isSigningUp,
        isSuccess: isSignUpSuccess,
    } = useMutation({
        ...createUserMutation(),
        onError: (error) => {
            if (error.detail) {
                toast(`${error.detail}`);
            } else {
                toast("A sign up error occured");
            }
        },
        onSuccess: ({ username }, { body: user }) => {
            toast(`User '${username}' Created Successfully`);
        },
    });

    function onSubmit(data: CreateUser) {

        signup({
            body: { ...data },
        });

        if (isSignUpSuccess) {
            login({
                body: {
                    username: data.username,
                    password: data.password,
                },
            });

            if (isLoggingIn) {
                return (<div className="flex justify-center items-center text-2xl">Logging in user...</div>);
            }
            if (isLoginError) {
                // manually login user
                router.push("/user/login");
                toast("failed... login in with the user you just created.");
            }
            if (isLoginSuccess) {
                // redirect them to dashboard or page they came from
                router.push("/dashboard");
            }
        }
    }

    return (
        <div className="sm:px-8 p-4 min-w-[50%]">
            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)}>
                    <div className="flex flex-col gap-10">
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
                                disabled={isLoggingIn}
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

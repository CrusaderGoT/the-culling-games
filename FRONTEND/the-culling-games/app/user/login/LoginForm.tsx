"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Form } from "@/components/ui/form";
import { InputWithLabel } from "@/components/inputs/InputWithLabel";
import { Button } from "@/components/ui/button";
import { LinkButton } from "@/components/LinkButton";
import { LogInIcon, UserPlus2Icon } from "lucide-react";
import { useAction } from "next-safe-action/hooks";
import { loginUserAction } from "@/api/actions/user-actions";

export const loginUserSchema = z.object({
    username: z
        .string()
        .nonempty({ message: "Username must be at least 2 characters" }),
    password: z
        .string()
        .min(8, { message: "Password must be atleast 8 characters" }),
});

type formSchemaType = z.infer<typeof loginUserSchema>;

export function LoginForm() {
    const form = useForm<formSchemaType>({
        resolver: zodResolver(loginUserSchema),
        defaultValues: {
            username: "",
            password: "",
        },
    });

    const {
        executeAsync: executeLogin,
        result: loginResult,
        isPending: isLoggingIn,
        reset: resetLoginAction,
    } = useAction(loginUserAction, {
        onSuccess({ data }) {
            if (data?.data) {
                // save token
                // redirect to prev page
            }
            // toast error message
        },
        onError() {
            // toast server error
            resetLoginAction()
        }
    })

    function onSubmit({ username, password }: formSchemaType) {
        // next safe action form here
        console.log(username, password);
    }

    return (
        <div className="sm:px-8 p-4 container w-max mx-auto my-[10%]">
            <div>
                <p className="font-bold text-lg">Log In</p>
            </div>
            <div className="p-3 border rounded-lg">
                <Form {...form}>
                    <form onSubmit={form.handleSubmit(onSubmit)}>
                        <div className="flex flex-col sm:flex-row gap-5 sm:justify-center">
                            <div className="flex flex-col gap-3 sm:flex-row">
                                <InputWithLabel<formSchemaType>
                                    fieldTitle="Username"
                                    nameInSchema="username"
                                />
                                <InputWithLabel<formSchemaType>
                                    fieldTitle="Password"
                                    nameInSchema="password"
                                    type="password"
                                />
                            </div>
                            <div className="mt-3 sm:m-0 max-w-xs h-max flex items-center justify-between sm:self-end gap-2">
                                <Button type="submit" className="flex text-center gap-1">
                                    Log In
                                    <div className="hidden sm:block">
                                        <LogInIcon />
                                    </div>
                                    
                                </Button>

                                <div className="self-center  font-semibold">
                                    <p>or</p>
                                </div>

                                <LinkButton
                                    href="/user/signup"
                                    label="Create Account"
                                    icon={UserPlus2Icon}
                                />
                            </div>
                        </div>
                    </form>
                </Form>
            </div>
        </div>
    );
}

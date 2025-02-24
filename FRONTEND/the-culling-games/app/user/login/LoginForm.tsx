"use client";

import { DisplayResponseMessage } from "@/components/DisplayServerResponse";
import { InputForm } from "@/components/inputs/InputForm";
import { LinkButton } from "@/components/LinkButton";
import { Button } from "@/components/ui/button";
import { Form } from "@/components/ui/form";
import { useLoginMutation } from "@/lib/custom-hooks/user-mutations";
import { zodResolver } from "@hookform/resolvers/zod";
import { LogInIcon, UserPlus2Icon } from "lucide-react";
import { useForm } from "react-hook-form";
import { z } from "zod";

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

    const { isPending, isSuccess, mutate, error } = useLoginMutation();

    function onSubmit(data: formSchemaType) {
        // tanstack mutation here
        mutate({
            body: { ...data },
        });
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
                                <InputForm<formSchemaType>
                                    fieldTitle="Username"
                                    nameInSchema="username"
                                />
                                <InputForm<formSchemaType>
                                    fieldTitle="Password"
                                    nameInSchema="password"
                                    type="password"
                                />
                            </div>

                            <div className="sm:self-end ">
                                {error && (
                                    <div className="max-w-xs my-1 max-h-max">
                                        <DisplayResponseMessage error={error} />
                                    </div>
                                )}

                                <div className="mt-3 sm:m-0 max-w-xs h-max flex items-center justify-between gap-2">
                                    <Button
                                        disabled={isPending || isSuccess}
                                        type="submit"
                                        className="flex text-center gap-1"
                                    >
                                        Log In
                                        <div className="hidden sm:block">
                                            <LogInIcon />
                                        </div>
                                    </Button>

                                    <div className="self-center  font-semibold">
                                        <p>or</p>
                                    </div>

                                    <LinkButton
                                        disabled={isSuccess}
                                        href="/user/signup"
                                        label="Create Account"
                                        icon={UserPlus2Icon}
                                    />
                                </div>
                            </div>
                        </div>
                    </form>
                </Form>
            </div>
        </div>
    );
}

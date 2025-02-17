"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Form } from "@/components/ui/form";
import { InputWithLabel } from "@/components/inputs/InputWithLabel";
import { Button } from "@/components/ui/button";
import { LinkButton } from "@/components/LinkButton";
import { LogInIcon, UserPlus2Icon } from "lucide-react";
import { useRouter } from "next/navigation";
import { useMutation } from "@tanstack/react-query";
import { createTokenMutation } from "@/api/client/@tanstack/react-query.gen";
import { toast } from "sonner";

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
    
    const router = useRouter();

    const form = useForm<formSchemaType>({
        resolver: zodResolver(loginUserSchema),
        defaultValues: {
            username: "",
            password: "",
        },
    });

    const { isPending, isSuccess, mutate, error } = useMutation({
        ...createTokenMutation(),
        onError: (error) => {
            if (error.detail) {
                toast(`${error.detail}`);
            } else {
                toast("An error occured");
            }
        },
        onSuccess: (data) => {
            // save token to cookie; did not work
            const tokenString = data.access_token;
            localStorage.setItem("access_token", tokenString)
            // invalidate prev user; refetch user query keys
            // redirect
            router.push("/dashboard")
        }
    });

    function onSubmit(data: formSchemaType) {
        // tanstack mutation here
        mutate({
            body: {...data}
        })
    }

    return (
        <div className="sm:px-8 p-4 container w-max mx-auto my-[10%]">
            <div>
                <p className="font-bold text-lg">Log In</p>
            </div>
            <div className="p-3 border rounded-lg">
                {
                    error?.detail ? (
                        <div>{error.detail.toLocaleString()}</div>
                    ) :
                    null
                }
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
                    </form>
                </Form>
            </div>
        </div>
    );
}

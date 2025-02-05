"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Form } from "@/components/ui/form";
import { InputWithLabel } from "@/components/inputs/InputWithLabel";
import { Button } from "@/components/ui/button";
import { LinkButton } from "@/components/LinkButton";
import { Link2Icon } from "lucide-react";

const formSchema = z.object({
    username: z
        .string()
        .nonempty({ message: "Username must be at least 2 characters" }),
    password: z
        .string()
        .min(8, { message: "Password must be atleast 8 characters" }),
});

type formSchemaType = z.infer<typeof formSchema>;

export function LoginForm() {
    const form = useForm<formSchemaType>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            username: "",
            password: "",
        },
    });

    function onSubmit({ username, password }: formSchemaType) {
        // next safe action form here
        console.log(username, password);
    }

    return (
        <div className="sm:px-8 p-4 m-10 container">
            <div>
                <p>Log In Here</p>
            </div>
            <Form {...form}>
                <form
                    onSubmit={form.handleSubmit(onSubmit)}
                    className="flex items-center justify-start p-3 border rounded !text-xs"
                >
                    <div className="flex flex-col sm:flex-row justify-around w-full">
                        <InputWithLabel<formSchemaType>
                            fieldTitle="Username"
                            nameInSchema="username"
                        />
                        <InputWithLabel<formSchemaType>
                            fieldTitle="Password"
                            nameInSchema="password"
                            type="password"
                        />
                        <div className="mt-3 sm:m-0 max-w-xs flex items-center justify-between sm:items-end gap-2">
                            <Button type="submit">
                                Log In
                            </Button>
                            <LinkButton
                                href="/user/signup"
                                label="Create Account"
                                icon={Link2Icon}
                            />
                        </div>
                    </div>
                </form>
            </Form>
        </div>
    );
}

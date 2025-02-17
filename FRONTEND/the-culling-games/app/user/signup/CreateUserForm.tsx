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
import { createUserMutation } from "@/api/client/@tanstack/react-query.gen";
import { toast } from "sonner";

export function CreateUserForm() {
    const defaultValues: CreateUser = {
        username: "ziniaiajc",
        email: "mdcocmd@email.com",
        country: Country.AD,
        password: "miewfjiiwe",
        confirm_password: "mfowekfowkfo",
    };

    const form = useForm<CreateUser>({
        resolver: zodResolver(zCreateUser),
        defaultValues: defaultValues,
    });

    const { mutate, isPending } = useMutation({
        ...createUserMutation(),
        onError: (error) => {
            if (error.detail) {
                toast(`${error.detail}`);
            } else {
                toast("An error occured");
            }
        },
        onSuccess: (data) => {
            toast(`User Created Successfully ${JSON.stringify(data)}`);
        },
    });

    function onSubmit(data: CreateUser) {
        console.log(data)
        mutate({
            body: {...data},
            headers: {
                "Access-Control-Allow-Origin": "*"
            },
            mode: "no-cors"
        });
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
                                disabled={isPending}
                                type="submit"
                                className="flex text-center gap-1"
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

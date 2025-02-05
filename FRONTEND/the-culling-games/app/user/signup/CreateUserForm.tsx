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
import { LogInIcon, PersonStandingIcon } from "lucide-react";

export function CreateUserForm() {
    const defaultValues: CreateUser = {
        username: "",
        email: "",
        country: Country.AD,
        password: "",
        confirm_password: "",
    };

    const form = useForm<CreateUser>({
        resolver: zodResolver(zCreateUser),
        defaultValues: defaultValues,
    });

    const countries = [{ id: "NG", description: "Nigeria" }];

    function onSubmit(data: CreateUser) {
        console.log({ ...data });
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
                                data={countries}
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
                                type="submit"
                                className="flex"
                                title="Create Account"
                            >
                                Create Account
                                <div className="hidden sm:block">
                                    <PersonStandingIcon />
                                </div>
                            </Button>

                            <div className="sm:self-center">
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

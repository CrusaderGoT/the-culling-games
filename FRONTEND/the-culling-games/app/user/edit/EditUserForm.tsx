"use client";

import { SelectWithLabel } from "@/components/inputs/SelectWithLabel";
import { type EditUser, UserInfo } from "@/api/client";
import { zEditUser,  } from "@/api/client/zod.gen";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Form } from "@/components/ui/form";
import { InputWithLabel } from "@/components/inputs/InputWithLabel";
import { Button } from "@/components/ui/button";
import { LinkButton } from "@/components/LinkButton";
import { LogInIcon, PersonStandingIcon } from "lucide-react";

type EditUserFormProp = {
    user: UserInfo,
}

export function EditUserForm({ user }: EditUserFormProp) {
    const defaultValues: EditUser = {
        username: user.username,
        email: user.email,
        country: user.country,
    };

    const form = useForm<EditUser>({
        resolver: zodResolver(zEditUser),
        defaultValues: defaultValues,
    });

    const countries = [{ id: "NG", description: "Nigeria" }];

    function onSubmit(data: EditUser) {
        console.log({ ...data });
    }

    return (
        <div className="sm:px-8 p-4 border rounded container">
            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)}>
                    <div className="flex flex-col gap-4 w-full max-w-xs">
                        <InputWithLabel<EditUser>
                            fieldTitle="Username"
                            nameInSchema="username"
                        />

                        <InputWithLabel<EditUser>
                            fieldTitle="Email"
                            nameInSchema="email"
                            type="email"
                            autoComplete="false"
                        />

                        <SelectWithLabel<EditUser>
                            data={countries}
                            fieldTitle="Country"
                            nameInSchema="country"
                        />

                        <div className="flex justify-between gap-3 sm:flex-row-reverse">
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

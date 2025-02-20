"use client";

import { type EditUser, UserInfo } from "@/api/client";
import { editUserMutation } from "@/api/client/@tanstack/react-query.gen";
import { zEditUser } from "@/api/client/zod.gen";
import { InputWithLabel } from "@/components/inputs/InputWithLabel";
import { SelectWithLabel } from "@/components/inputs/SelectWithLabel";
import { Button } from "@/components/ui/button";
import { Form } from "@/components/ui/form";
import { COUNTRIES } from "@/constants/COUNTRIES";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";
import { Edit3Icon } from "lucide-react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";

type EditUserFormProp = {
    user: UserInfo;
};

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

    const { isPending, mutate } = useMutation({
        ...editUserMutation(),
        onError: (error) => {
            if (error.detail) {
                toast(`${error.detail}`);
            } else {
                toast(`${error ? error : "An error occured"}`);
            }
        },
        onSuccess: () => {
            toast("Edited successfully");
        },
    });

    function onSubmit(data: EditUser) {
        const token = localStorage.getItem("access_token");
        mutate({
            path: {
                user: user.id,
            },
            body: { ...data },
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
    }

    return (
        <div className="sm:px-8 p-4 border rounded container h-max w-max mx-auto my-[10%]">
            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)}>
                    <div className="flex flex-col gap-4 md:flex-row">
                        <div className="flex flex-col sm:flex-row gap-5 sm:justify-center">
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
                                data={COUNTRIES}
                                fieldTitle="Country"
                                nameInSchema="country"
                            />
                        </div>

                        <div className="self-end">
                            <Button
                                type="submit"
                                className="flex"
                                title="Edit User"
                                disabled={isPending}
                            >
                                Edit User
                                <div className="hidden sm:block">
                                    <Edit3Icon />
                                </div>
                            </Button>
                        </div>
                    </div>
                </form>
            </Form>
        </div>
    );
}

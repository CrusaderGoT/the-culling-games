"use client";

import { SelectWithLabel } from "@/components/inputs/SelectWithLabel";
import {
  type CreateUser,
  type EditUser,
  UserInfo,
  Country,
} from "@/api/client";
import { zCreateUser, zEditUser } from "@/api/client/zod.gen";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Form } from "@/components/ui/form";
import { InputWithLabel } from "@/components/inputs/InputWithLabel";
import { Button } from "@/components/ui/button";
import { LinkButton } from "@/components/LinkButton";
import { LogInIcon, PersonStandingIcon } from "lucide-react";

type UserFormProp<T extends CreateUser | EditUser> = {
  user?: UserInfo;
  schema: T extends CreateUser ? typeof zCreateUser : typeof zEditUser;
};

export function UserForm<T extends CreateUser | EditUser>({
  user,
  schema,
}: UserFormProp<T>) {

  type schemaType = T extends CreateUser ? CreateUser : EditUser;

  const defaultValues: Partial<schemaType> = {
    username: user?.username ?? "",
    email: user?.email ?? "",
    country: user?.country ?? Country.NG,
    // Only include password fields if T is CreateUser
    ...(schema === zCreateUser ? { password: "", confirm_password: "" } : {}),
  } as schemaType;

  const form = useForm<schemaType>({
    resolver: zodResolver(schema),
    defaultValues: defaultValues as DefaultValues<schemaType>,
  });

  const countries = [{ id: "AF", description: "Anambra" }];

  function onSubmit(data: CreateUser) {
    console.log({ ...data });
  }

  return (
    <div className="flex flex-col gap-1 sm:px-8 p-4 rounded">
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)}>
          <div className="flex flex-col gap-4 w-full max-w-xs">
            {user ? (
              <InputWithLabel<typeof user>
                fieldTitle="Username"
                nameInSchema="username"
                value={user.username}
              />
            ) : (
              <InputWithLabel<CreateUser>
                fieldTitle="Username"
                nameInSchema="username"
                autoComplete="false"
              />
            )}

            {user ? (
              <InputWithLabel<typeof user>
                fieldTitle="Email"
                nameInSchema="email"
                type="email"
                value={user.username}
              />
            ) : (
              <InputWithLabel<CreateUser>
                fieldTitle="Email"
                nameInSchema="email"
                type="email"
                autoComplete="false"
              />
            )}

            {user ? (
              <SelectWithLabel<typeof user>
                data={countries}
                fieldTitle="Country"
                nameInSchema="country"
              />
            ) : (
              <SelectWithLabel<CreateUser>
                data={countries}
                fieldTitle="Country"
                nameInSchema="country"
              />
            )}

            {user ? null : (
              <InputWithLabel<CreateUser>
                fieldTitle="Password"
                nameInSchema="password"
                type="password"
                autoComplete="off"
                aria-autocomplete="none"
              />
            )}

            {user ? null : (
              <InputWithLabel<CreateUser>
                fieldTitle="Confirm Password"
                nameInSchema="confirm_password"
                type="password"
                autoComplete="off"
                aria-autocomplete="none"
              />
            )}

            <div className="flex justify-between gap-3 sm:flex-row-reverse">
              {user ? (
                <div>Edit User</div>
              ) : (
                <>
                  <Button type="submit" className="flex" title="Create Account">
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
                </>
              )}
            </div>
          </div>
        </form>
      </Form>
    </div>
  );
}

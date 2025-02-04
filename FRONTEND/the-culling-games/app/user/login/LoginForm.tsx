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
    console.log(username);
  }

  return (
    <Form {...form}>
      <form
        onSubmit={form.handleSubmit(onSubmit)}
        className="border rounded p-2"
      >
        <div className="flex flex-col justify-between">
          <InputWithLabel<formSchemaType>
            fieldTitle="Username"
            nameInSchema="username"
          />
          <InputWithLabel<formSchemaType>
            fieldTitle="Password"
            nameInSchema="password"
          />
          <div>
            <Button type="submit" className="my-3">
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
  );
}

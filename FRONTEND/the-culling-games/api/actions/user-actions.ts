"use server"

import { actionClient } from "@/lib/safe-actions";
import { AuthService, UsersService} from "../client";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { loginUserSchema } from "@/app/user/login/LoginForm";
import { flattenValidationErrors } from "next-safe-action";
import { z } from "zod";

export async function getCurrentUser() {
    const accessToken = (await cookies()).get("access_token");

    if (!accessToken) redirect("/user/login");

    const userResponse = await UsersService.currentUser({
        headers: {
            Authorization: `Bearer ${accessToken}`
        }
    });

    return userResponse;
}

export const loginUserAction = actionClient
    .metadata({ actionName: "loginUserAction" })
    .schema(loginUserSchema, {
        handleValidationErrorsShape: async (ve) => flattenValidationErrors(ve).fieldErrors,
    })
    .action(async ({
        parsedInput: { username, password }
    }: { parsedInput: z.infer<typeof loginUserSchema> }) => {

        const tokenResponse = await AuthService.createToken({
            body: { username: username, password: password }
        });

        return tokenResponse;
    })
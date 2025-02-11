import { PlayerForm } from "./PlayerForm";
import { PlayersService } from "@/api/client";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";


export default async function Page() {

    // try and fetch player
    `const token = (await cookies()).get("access_token");
    if (!token) {
        // no user is logged in; redirect to login page
        redirect("/user/login")
    }
    const playerResponse = await PlayersService.myPlayer({
        headers: {
            Authorization: Bearer {token}
        }
    })

    // check is playerResponse return an error
    if (playerResponse.error) {
        throw new Error("Error fetching Player")
    }`
    return (
        <div className="p-2">
            <div>
                <p className="font-semibold">
                    Create Your Player Here
                </p>
            </div>
            <PlayerForm />
        </div>
    )
}
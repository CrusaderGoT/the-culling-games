"use client"

import { CreatePlayerForm } from "./CreatePlayerForm";
import { useMyPlayerQuery } from "@/lib/custom-hooks/player-queries";
import { useRouter } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { currentUserOptions } from "@/api/client/@tanstack/react-query.gen";
import { LoaderCircle } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function CreatePlayerPage() {
    const router = useRouter()
    // get access token
    const token = localStorage.getItem("access_token")
    // check if player exists for this user, and if user exist
    const { data: currentUser, error, isPending, isSuccess, refetch } = useQuery({
        ...currentUserOptions({
            headers: {
                Authorization: `Bearer ${token}`
            }
        }),
    })
    return (
        <div>
            {isPending && (
                <div>
                    <LoaderCircle className="animate-spin" />
                </div>
            )}

            {error && (
                <div>
                    {error.message && error instanceof Error && (
                        <div>
                            <p>
                                {error.message}, make sure you have good
                                internet connection.
                            </p>
                            <Button onClick={() => refetch()}>Retry</Button>
                        </div>
                    )}

                    {error.detail && (
                        <div>
                            <p>{error.detail}</p>{" "}
                            <Button
                                onClick={(e) => {
                                    e.currentTarget.disabled;
                                    router.push("/user/login");
                                }}
                            >
                                Login
                            </Button>
                        </div>
                    )}

                    {typeof error === "string" && (
                        <div>
                            <p>{error}</p>
                            <Button
                                onClick={() => router.push("/player/edit")}
                            >
                                Edit Player
                            </Button>
                        </div>
                    )}
                </div>
            )}

            {currentUser && isSuccess && <CreatePlayerForm user={currentUser} />}
        </div>
    );
}

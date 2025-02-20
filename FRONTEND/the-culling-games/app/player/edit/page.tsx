"use client";

import { Button } from "@/components/ui/button";
import { useMyPlayerQuery } from "@/lib/custom-hooks/player-queries";
import { LoaderCircle } from "lucide-react";
import { useRouter } from "next/navigation";
import { EditPlayerForm } from "./EditPlayerForm";
import clsx from "clsx";

export default function Page() {
    const router = useRouter();

    const token = localStorage.getItem("access_token");

    const {
        data: myPlayer,
        error,
        refetch,
        isPending,
        isSuccess,
    } = useMyPlayerQuery(token);

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
                                onClick={() => router.push("/player/create")}
                            >
                                Create Player
                            </Button>
                        </div>
                    )}
                </div>
            )}

            {myPlayer && isSuccess && <EditPlayerForm player={myPlayer} />}
        </div>
    );
}

import { APlayerPage } from "./APlayerPage";
import { MyPlayerPage } from "./MyPlayerPage";

export default async function PlayerPage({
    searchParams,
}: {
    searchParams: Promise<{ [key: string]: string | undefined }>;
}) {
    const { playerId } = await searchParams;

    if (!playerId) return <MyPlayerPage />;

    return (
        <APlayerPage playerId={playerId} />
    )
}

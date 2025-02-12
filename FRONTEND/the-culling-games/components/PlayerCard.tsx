import { Card, CardHeader, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";

export function PlayerCard2() {
    // get player from api
    return (
        <div
            className="flex flex-col px-3 py-1 rounded-xl gap-9 lg:w-[50%]
							bg-gradient-radial from-pink-600 from-50% to-violet-700"
        >
            <div className="flex justify-between gap-3 text-nowrap">
                <span>points</span>
                <span>grade</span>
            </div>

            <div className="self-center">
                <span>Player Name</span>
            </div>

            <div className="flex justify-between gap-3 text-nowrap">
                <span>wins</span>
                <span>stats</span>
            </div>
        </div>
    );
}

export function PlayerCard() {
  const player = {
    name: "John Doe",
    grade: "A",
    gender: "Male",
    points: 1200,
    created: new Date(),
    // Removed extra cursed technique details for minimalism
  };

  return (
    <Card className="shadow-sm bg-gradient-radial from-pink-600 from-50% to-violet-700">
      <CardHeader className="flex flex-col justify-between items-center border-b pb-3">
        <Avatar className="w-16 h-16 mb-2">
          <AvatarImage src="/placeholder-avatar.png" alt={player.name} />
          <AvatarFallback>{player.name.charAt(0)}</AvatarFallback>
        </Avatar>
        <h2 className="text-lg font-bold">{player.name}</h2>
        <Badge variant="secondary" className="text-xs mt-1 max-h-max">
          Grade {player.grade}
        </Badge>
      </CardHeader>
      <CardContent className="p-4">
        <div className="flex justify-between text-sm mb-1">
          <span>Gender:</span>
          <span>{player.gender}</span>
        </div>
        <div className="flex justify-between text-sm mb-1">
          <span>Points:</span>
          <span>{player.points}</span>
        </div>
        <div className="flex justify-between text-sm">
          <span>Joined:</span>
          <span>{player.created.toLocaleDateString()}</span>
        </div>
      </CardContent>
    </Card>
  );
}
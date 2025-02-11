import { Card, CardHeader, CardContent, CardFooter } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

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
        cursed_technique: {
            name: "Shadow Manipulation",
            definition: "Allows the user to manipulate shadows.",
            applications: [
                { id: 1, application: "Stealth" },
                { id: 2, application: "Attack" },
                { id: 3, application: "Defense" },
            ],
        },
    };
    return (
      <Card className="w-full max-w-md bg-gradient-radial from-pink-600 from-50% to-violet-700 text-white">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <h2 className="text-2xl font-bold">{player.name}</h2>
        
          <Badge variant="secondary" className="text-sm">
            Grade {player.grade}
          </Badge>
        </CardHeader>
        <CardContent className="space-y-2">
          <div className="flex justify-between items-center">
            <span className="text-sm">Gender</span>
            <span className="font-semibold capitalize">{player.gender}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm">Points</span>
            <span className="font-semibold">{player.points}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm">Joined</span>
            <span className="font-semibold">{player.created.toLocaleDateString()}</span>
          </div>
        </CardContent>
        <CardFooter className="flex flex-col items-start">
          <h3 className="text-lg font-semibold mb-2">Cursed Technique</h3>
          <p className="font-medium mb-1">{player.cursed_technique.name || "Unnamed Technique"}</p>
          <p className="text-sm mb-2">{player.cursed_technique.definition || "No definition available"}</p>
          <div className="w-full">
            <h4 className="text-sm font-semibold mb-1">Applications:</h4>
            <div className="flex flex-wrap gap-2">
              {player.cursed_technique.applications.map((app) => (
                <Badge key={app.id} variant="outline" className="text-xs">
                  {app.application}
                </Badge>
              ))}
            </div>
          </div>
        </CardFooter>
      </Card>
    )
  }
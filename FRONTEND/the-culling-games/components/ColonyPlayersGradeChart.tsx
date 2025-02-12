"use client"

import * as React from "react"
import { TrendingUp } from "lucide-react"
import { Label, Pie, PieChart } from "recharts"

import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { type ChartConfig, ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart"

// Imagine this data is coming in as a prop or from a fetch
const colony = {
  players: [
    { id: 1, created: "2025-01-01", grade: 0, points: 10.0 },
    { id: 2, created: "2025-01-02", grade: 0, points: 20.0 },
    { id: 3, created: "2025-01-03", grade: 0, points: 30.0 },
    { id: 4, created: "2025-01-04", grade: 0, points: 15.0 },
    { id: 5, created: "2025-01-05", grade: 4, points: 25.0 },
    { id: 6, created: "2025-01-06", grade: 4, points: 18.0 },
    { id: 7, created: "2025-01-07", grade: 4, points: 22.0 },
    { id: 8, created: "2025-01-08", grade: 4, points: 12.0 },
    { id: 9, created: "2025-01-09", grade: 4, points: 28.0 },
    { id: 10, created: "2025-01-10", grade: 4, points: 19.0 },
    { id: 11, created: "2025-01-11", grade: 2, points: 24.0 },
    { id: 12, created: "2025-01-12", grade: 0, points: 11.0 },
    { id: 13, created: "2025-01-13", grade: 3, points: 27.0 },
    { id: 14, created: "2025-01-14", grade: 1, points: 21.0 },
    { id: 15, created: "2025-01-15", grade: 2, points: 23.0 },
    { id: 16, created: "2025-01-16", grade: 0, points: 13.0 },
    { id: 17, created: "2025-01-17", grade: 3, points: 29.0 },
    { id: 18, created: "2025-01-18", grade: 1, points: 17.0 },
    { id: 19, created: "2025-01-19", grade: 2, points: 26.0 },
    { id: 20, created: "2025-01-20", grade: 0, points: 14.0 },
  ],
}

const GRADE_MAPPING = [
  { grade: 0, label: "Grade 0", player: 0, fill: "#8B5CF6" }, // Violet
  { grade: 1, label: "Grade 1", player: 0, fill: "#EC4899" }, // Pink
  { grade: 2, label: "Grade 2", player: 0, fill: "#10B981" }, // Emerald
  { grade: 3, label: "Grade 3", player: 0, fill: "#F59E0B" }, // Amber
  { grade: 4, label: "Grade 4", player: 0, fill: "red" }, // Red
]

function transformPlayerToChartData(Colony: typeof colony, mapping: typeof GRADE_MAPPING): typeof GRADE_MAPPING {
  const result = [...mapping]
  Colony.players.forEach((player) => {
    const gradeIndex = result.findIndex((item) => item.grade === player.grade)
    if (gradeIndex !== -1) {
      result[gradeIndex].player++
    }
  })
  return result
}

const chartConfig: ChartConfig = {
  player: {
    label: "Players",
  },
  ...Object.fromEntries(
    GRADE_MAPPING.map((grade) => [
      grade.grade,
      {
        label: grade.label,
        color: grade.fill,
      },
    ]),
  ),
}

export function ColonyPlayerGradeChart() {
  const chartData = React.useMemo(() => transformPlayerToChartData(colony, GRADE_MAPPING), [])
  const totalPlayers = React.useMemo(() => chartData.reduce((acc, curr) => acc + curr.player, 0), [chartData])

  return (
    <Card className="flex flex-col">
      <CardHeader className="items-center pb-0">
        <CardTitle>Colony Player Grade Distribution</CardTitle>
        <CardDescription>Current Player Grades</CardDescription>
      </CardHeader>
      <CardContent className="flex-1 pb-0">
        <ChartContainer config={chartConfig} className="mx-auto aspect-square max-h-[250px]">
          <PieChart>
            <ChartTooltip cursor={false} content={<ChartTooltipContent />} />
            <Pie data={chartData} dataKey="player" nameKey="label" innerRadius={60} strokeWidth={5}>
              <Label
                content={({ viewBox }) => {
                  if (viewBox && "cx" in viewBox && "cy" in viewBox) {
                    return (
                      <text x={viewBox.cx} y={viewBox.cy} textAnchor="middle" dominantBaseline="middle">
                        <tspan x={viewBox.cx} y={viewBox.cy} className="fill-foreground text-3xl font-bold">
                          {totalPlayers.toLocaleString()}
                        </tspan>
                        <tspan x={viewBox.cx} y={(viewBox.cy || 0) + 24} className="fill-muted-foreground">
                          Players
                        </tspan>
                      </text>
                    )
                  }
                }}
              />
            </Pie>
          </PieChart>
        </ChartContainer>
      </CardContent>
      <CardFooter className="flex-col gap-2 text-sm">
        <div className="flex items-center gap-2 font-medium leading-none">
          Current player grade distribution
          <TrendingUp className="h-4 w-4" />
        </div>
        <div className="leading-none text-muted-foreground">Showing total players across 4 grades</div>
      </CardFooter>
    </Card>
  )
}


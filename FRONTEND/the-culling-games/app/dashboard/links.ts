// for the links in the dashboard
import { LogOutIcon, HomeIcon, FishIcon, ChartLineIcon, FlameIcon } from "lucide-react";


export const links = [
  {
    icon: HomeIcon,
    name: 'Home',
    href: '/dashboard',
  },
  {
    icon: FishIcon,
    name: 'Players',
    href: '/dashboard/players',
  },
  {
    icon: FlameIcon,
    name: 'matches',
    href: '/dashboard',
  },
  {
    icon: ChartLineIcon,
    name: 'stats for charts/leaderboard, etc.',
    href: '/dashboard',
  },
  
  {
    icon: LogOutIcon,
    name: 'log out',
    href: '/dashboard',
  },
]
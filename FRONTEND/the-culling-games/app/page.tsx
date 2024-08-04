"use server"

import { getUser } from "./actions";

export default async function Home() {
  const user = await getUser()
  return (
    <>
      <main className={`w-full h-screen border border-red-600 items-center justify-between font-mono text-sm`}>
        WELCOME TO THE CULLING GAMES HOME PAGE
        {user.username}
        {user.id}
      </main>
    </>
  );
}


// handles form actions 

import { cookies } from "next/headers";

export async function getUser() {
  const tokenCookie = cookies().get('token')
  const res = await fetch('http://localhost:8000/users/me', {
    headers: {
      'accept': 'application/json',
      'Authorization': `Bearer ${tokenCookie?.value}`,
    },
    next: { revalidate: 30 }
  });

  if (!res.ok) {
    throw new Error(`Failed to get user: ${res.statusText}`);
  }

  return res.json();

}


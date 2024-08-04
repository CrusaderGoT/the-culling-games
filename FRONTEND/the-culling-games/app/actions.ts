// handles form actions 

export async function getUser() {
  const res = await fetch('http://localhost:8000/users/me', {
    headers: {
      'accept': 'application/json',
      'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZWRiIjoiY3J1c2FkZXIiLCJleHBpcmVzIjoiMjAyNC0wNy0zMFQyMToxODozNi4zNzMyODgrMDA6MDAifQ.nJAvsiQ6KWf8L5OevGi9R9FoKYmXj74Pm4_s8cF227Q',
    },
    next: { revalidate: 30 }
  });

  if (!res.ok) {
    throw new Error(`Failed to get user: ${res.statusText}`);
  }

  return res.json();

}


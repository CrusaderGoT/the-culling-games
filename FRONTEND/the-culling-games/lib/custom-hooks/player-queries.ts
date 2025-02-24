import { myPlayerOptions } from "@/api/client/@tanstack/react-query.gen";
import { useQuery } from "@tanstack/react-query";

export const useMyPlayerQuery = (access_token: string | null) => {
    return useQuery({
        ...myPlayerOptions({
            headers: {
                Authorization: `Bearer ${access_token}`
            }
        }),
        retry: Infinity,
    })
}
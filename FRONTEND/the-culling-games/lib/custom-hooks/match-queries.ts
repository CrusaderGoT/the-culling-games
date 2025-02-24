"use client";

import { getLastestMatchOptions } from "@/api/client/@tanstack/react-query.gen";
import { useQuery } from "@tanstack/react-query";

export const useLatestMatchQuery = (token: string | null) => {

  return useQuery({
    ...getLastestMatchOptions({
      headers: {
        Authorization: `Bearer ${token}`,
      },
      query: {
        ongoing: false,
      },
    })
  });
};

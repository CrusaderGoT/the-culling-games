"use client"

import {
  createTokenMutation,
  createUserMutation,
} from "@/api/client/@tanstack/react-query.gen";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { toast } from "sonner";



export const useLoginMutation = () => {
  const router = useRouter();

  const queryClient = useQueryClient();

  const mutationKey = ["createToken"];

  return useMutation({
    ...createTokenMutation(),
    mutationKey: mutationKey,
    onError: (error) => {
      if (error.detail) {
        toast(
          `${
            typeof error?.detail === "string"
              ? error.detail
              : "A log in error occurred"
          }`
        );
      } else if (error instanceof Error) {
        toast(error.message);
      } else {
        toast("a login error occured");
      }
    },
    onSuccess: (data) => {
      // save token to cookie; did not work
      const tokenString = data.access_token;
      localStorage.setItem("access_token", tokenString);
      // invalidate/refetch all queries, as this user just log in
      queryClient.invalidateQueries();
      // redirect
      router.push("/dashboard");
    },
  });
};

export const useSignUpMutation = () => {
  const queryClient = useQueryClient();

  return useMutation({
    ...createUserMutation(),
    onError: (error) => {
      if (error.detail) {
        toast(
          `${
            typeof error?.detail === "string"
              ? error.detail
              : "A sign up error occurred"
          }`
        );
      } else {
        toast("A sign up error occurred");
      }
    },
    onSuccess: (data) => {
      toast(`User '${data.username}' created successfully`);
      // invalidate/refetch all queries, as this user was just created
      queryClient.invalidateQueries();
    },
    retry: 3,
  });
};

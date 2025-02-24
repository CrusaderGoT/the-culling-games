import {
  createPlayerMutation,
  editPlayerMutation,
} from "@/api/client/@tanstack/react-query.gen";
import { useMutation } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { toast } from "sonner";

export const useCreatePlayerMutation = (token: string | null) => {
  const router = useRouter();

  return useMutation({
    ...createPlayerMutation({
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }),
    onError: (error) => {
      if (error.detail) {
        toast(
          `${
            typeof error?.detail === "string"
              ? error.detail
              : "A Error Occured While Creating Player"
          }`
        );
      } else if (error instanceof Error) {
        toast(error.message);
      } else {
        toast("A Error Occured While Creating Player");
      }
    },
    onSuccess: (data) => {
      toast(`Player '${data.name}', Created Succesffully`);
      // redirect
      router.push("/dashboard");
    },
  });
};

export const useEditPlayerMutation = (token: string | null) => {
  return useMutation({
    ...editPlayerMutation({
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }),
    onError: (error) => {
      if (error.detail) {
        toast(
          `${
            typeof error?.detail === "string"
              ? error.detail
              : "A Error Occured While Editing Player"
          }`
        );
      } else if (error instanceof Error) {
        toast(error.message);
      } else {
        toast("A Error Occured While Editing Player");
      }
    },
    onSuccess: (data) => {
      toast(`Player '${data.name}', Edited Succesffully`);
    },
  });
};

import { defineConfig } from "@hey-api/openapi-ts";

export default defineConfig({
  input: "http://localhost:8000/openapi.json",
  output: {
    format: "prettier",
    lint: "eslint",
    path: "api/client",
  },
  plugins: [
    {
      name: "@hey-api/client-next",
      runtimeConfigPath: "./api/hey-api.ts",
    },
    {
      name: "@hey-api/sdk",
      asClass: true,
      validator: "zod",
      transformer: "@hey-api/transformers",
    },
    {
      name: "@hey-api/typescript",
      enums: "javascript"
    },
    "zod",
    "@hey-api/transformers",
    "@tanstack/react-query",
    
    
  ],
  watch: true, // true to keep check for changes to fastapi openapi specs
});

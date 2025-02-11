import { defineConfig } from "@hey-api/openapi-ts";
import { defaultPlugins } from '@hey-api/openapi-ts';

export default defineConfig({
  input: "http://localhost:8000/openapi.json",
  output: {
    format: "prettier",
    lint: "eslint",
    path: "api/client",
  },
  plugins: [
    ...defaultPlugins,
    "zod",
    '@hey-api/transformers',
    {
      name: "@hey-api/client-next",
      runtimeConfigPath: "./api/hey-api.ts",
    },
    {
      asClass: true,
      name: "@hey-api/sdk",
      validator: true,
      transformer: true, 
    },
    {
      enums: "javascript",
      name: "@hey-api/typescript",
    },
  ],
  watch: false, // true to keep check for changes to fastapi openapi specs
});

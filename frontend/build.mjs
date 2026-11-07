// Compiles the React source (JSX) into a single minified bundle in dist/.
import { build } from "esbuild";
import { cpSync, mkdirSync, rmSync } from "node:fs";

rmSync("dist", { recursive: true, force: true });
mkdirSync("dist", { recursive: true });
const r = await build({
  entryPoints: ["src/main.jsx"], bundle: true, minify: true, sourcemap: true,
  outfile: "dist/app.js", jsx: "automatic", target: ["es2019"], metafile: true,
  define: { "process.env.NODE_ENV": '"production"' }, logLevel: "info",
});
for (const f of ["index.html", "manifest.json", "src/app.css"]) cpSync(f, "dist/" + f.split("/").pop());
console.log("Build OK:", Object.keys(r.metafile.outputs).filter((o) => !o.endsWith(".map")).join(", "));

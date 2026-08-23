import { build } from "esbuild";

build({
  entryPoints: ["./index.js"], // entry file
  outfile: "dist/index.js", // output file
  bundle: true, // bundle dependencies
  platform: "node", // for Node.js
  target: ["node18"], // target Node.js version
  sourcemap: true, // add source maps
  minify: false, // set true for prod
}).catch(() => process.exit(1));

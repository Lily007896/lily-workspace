import Exa from "exa-js";

const apiKey = process.env.EXA_API_KEY;
if (!apiKey) {
  console.error("Missing EXA_API_KEY. Set it first, e.g. export EXA_API_KEY=...");
  process.exit(1);
}

const argv = process.argv.slice(2);
const opts = {
  type: "auto",
  category: undefined,
  numResults: 5,
  userLocation: undefined,
  highlights: 500,
};

const queryParts = [];
for (let i = 0; i < argv.length; i++) {
  const a = argv[i];
  if (a === "--type") opts.type = argv[++i] || opts.type;
  else if (a === "--category") opts.category = argv[++i] || undefined;
  else if (a === "--num") opts.numResults = Number(argv[++i] || opts.numResults);
  else if (a === "--loc") opts.userLocation = argv[++i] || undefined;
  else if (a === "--highlights") opts.highlights = Number(argv[++i] || opts.highlights);
  else queryParts.push(a);
}

const query = queryParts.join(" ").trim();
if (!query) {
  console.error(
    "Usage: node scripts/exa-search.mjs [--type auto|fast|neural|deep|deep-reasoning|instant] [--category \"news\"] [--num 10] [--loc GB] [--highlights 800] \"your query\""
  );
  process.exit(1);
}

const exa = new Exa(apiKey);

const request = {
  type: opts.type,
  numResults: Number.isFinite(opts.numResults) ? opts.numResults : 5,
  contents: {
    highlights: {
      maxCharacters: Number.isFinite(opts.highlights) ? opts.highlights : 500,
    },
  },
};

if (opts.category) request.category = opts.category;
if (opts.userLocation) request.userLocation = opts.userLocation;

const result = await exa.search(query, request);

for (const [i, r] of (result.results || []).entries()) {
  console.log(`\n${i + 1}. ${r.title || "(no title)"}`);
  console.log(r.url || "");
  const hl = r.highlights?.[0] || "";
  if (hl) console.log(hl.replace(/\s+/g, " ").slice(0, 350));
}

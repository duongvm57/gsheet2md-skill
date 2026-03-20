const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const packageJson = JSON.parse(
  fs.readFileSync(path.join(__dirname, "..", "package.json"), "utf8")
);

test("package.json includes publish-ready npm metadata", () => {
  assert.deepEqual(packageJson.publishConfig, {
    access: "public",
  });
  assert.ok(Array.isArray(packageJson.keywords));
  assert.ok(packageJson.keywords.includes("codex"));
  assert.ok(packageJson.keywords.includes("cursor"));
  assert.ok(packageJson.keywords.includes("claude-code"));
  assert.ok(packageJson.keywords.includes("skill"));
  assert.equal(packageJson.name, "gsheet2md");
  assert.equal(packageJson.version, "0.3.0");
  assert.equal(packageJson.skills.name, "gsheet2md");
  assert.ok(packageJson.files.includes("skills"));
});

test("package.json exposes a release smoke-test script", () => {
  assert.equal(
    packageJson.scripts["release:check"],
    "npm test && npm pack --dry-run"
  );
});

test("README documents release verification and publish flow", () => {
  const readme = fs.readFileSync(path.join(__dirname, "..", "README.md"), "utf8");

  assert.match(readme, /npm pack --dry-run/);
  assert.match(readme, /npm publish --access public/);
  assert.match(readme, /release:check/);
  assert.match(readme, /npx skills add/);
  assert.match(readme, /`\.\/docs` of the current workspace/);
  assert.match(readme, /If `\.\/docs` does not exist, create it/);
  assert.match(readme, /--gid/);
});

test("skill examples and docs mention gid-based sheet selection", () => {
  const skillDoc = fs.readFileSync(
    path.join(__dirname, "..", "skills", "gsheet2md", "SKILL.md"),
    "utf8"
  );
  const jsonExample = fs.readFileSync(
    path.join(__dirname, "..", "skills", "gsheet2md", "examples", "read-sheet-json.sh"),
    "utf8"
  );
  const tableExample = fs.readFileSync(
    path.join(__dirname, "..", "skills", "gsheet2md", "examples", "read-sheet-table.sh"),
    "utf8"
  );

  assert.match(skillDoc, /--gid/);
  assert.match(skillDoc, /gid.*overrides.*sheet-name/i);
  assert.match(jsonExample, /--gid "<GID>"/);
  assert.match(tableExample, /--gid "<GID>"/);
});

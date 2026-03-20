const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

test("skills.sh-compatible skill assets exist under skills/gsheet2md", () => {
  const skillDir = path.join(__dirname, "..", "skills", "gsheet2md");
  const skillDoc = fs.readFileSync(path.join(skillDir, "SKILL.md"), "utf8");

  assert.equal(fs.existsSync(path.join(skillDir, "SKILL.md")), true);
  assert.equal(fs.existsSync(path.join(skillDir, "scripts", "read_sheet.py")), true);
  assert.match(skillDoc, /^---\nname: gsheet2md\ndescription: /);
  assert.match(skillDoc, /`\.\/docs`/);
  assert.match(skillDoc, /If `\.\/docs` does not exist, create it/);
  assert.doesNotMatch(skillDoc, /Save the markdown document under `docs\/`/);
  assert.doesNotMatch(skillDoc, /~\/\.codex\/skills|~\/\.claude\/skills|~\/\.cursor\/skills|~\/\.agent\/skills/);
});

test("skills repo includes troubleshooting and runnable examples", () => {
  const rootDir = path.join(__dirname, "..");

  assert.equal(
    fs.existsSync(path.join(rootDir, "skills", "gsheet2md", "docs", "troubleshooting.md")),
    true
  );
  assert.equal(
    fs.existsSync(path.join(rootDir, "skills", "gsheet2md", "examples", "read-sheet-json.sh")),
    true
  );
  assert.equal(
    fs.existsSync(path.join(rootDir, "skills", "gsheet2md", "examples", "read-sheet-table.sh")),
    true
  );
});

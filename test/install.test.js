const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");

const { installSkill } = require("../src/install");

test("installSkill copies skill assets into destination directory", async () => {
  const workspace = fs.mkdtempSync(path.join(os.tmpdir(), "gsr-install-"));
  const assetRoot = path.join(workspace, "assets");
  const destDir = path.join(workspace, "dest", "gsheet2md");

  fs.mkdirSync(path.join(assetRoot, "scripts"), { recursive: true });
  fs.writeFileSync(
    path.join(assetRoot, "SKILL.md"),
    "---\nname: gsheet2md\n---\n"
  );
  fs.writeFileSync(
    path.join(assetRoot, "scripts", "read_sheet.py"),
    "#!/usr/bin/env python3\nprint('ok')\n"
  );
  fs.writeFileSync(path.join(assetRoot, "package.json"), "{\"name\":\"ignored\"}\n");

  const result = await installSkill({
    assetRoot,
    destDir,
  });

  assert.equal(result.installed, true);
  assert.equal(result.destDir, destDir);
  assert.equal(
    fs.readFileSync(path.join(destDir, "SKILL.md"), "utf8"),
    "---\nname: gsheet2md\n---\n"
  );
  assert.equal(
    fs.readFileSync(path.join(destDir, "scripts", "read_sheet.py"), "utf8"),
    "#!/usr/bin/env python3\nprint('ok')\n"
  );
  assert.equal(fs.existsSync(path.join(destDir, "package.json")), false);
});

test("installSkill replaces existing contents in destination directory", async () => {
  const workspace = fs.mkdtempSync(path.join(os.tmpdir(), "gsr-install-"));
  const assetRoot = path.join(workspace, "assets");
  const destDir = path.join(workspace, "dest", "gsheet2md");

  fs.mkdirSync(path.join(assetRoot, "scripts"), { recursive: true });
  fs.mkdirSync(path.join(destDir, "scripts"), { recursive: true });
  fs.writeFileSync(path.join(assetRoot, "SKILL.md"), "new skill");
  fs.writeFileSync(path.join(assetRoot, "scripts", "read_sheet.py"), "new script");
  fs.writeFileSync(path.join(destDir, "SKILL.md"), "old skill");
  fs.writeFileSync(path.join(destDir, "scripts", "read_sheet.py"), "old script");

  await installSkill({
    assetRoot,
    destDir,
  });

  assert.equal(fs.readFileSync(path.join(destDir, "SKILL.md"), "utf8"), "new skill");
  assert.equal(
    fs.readFileSync(path.join(destDir, "scripts", "read_sheet.py"), "utf8"),
    "new script"
  );
});

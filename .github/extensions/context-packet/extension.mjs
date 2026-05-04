// Extension: context-packet

import { joinSession } from "@github/copilot-sdk/extension";
import { readFile } from "node:fs/promises";
import { dirname, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const extensionDir = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(extensionDir, "../../..");
const skillDir = resolve(repoRoot, "plugins/context-packet/skills/context-packet");
const skillPath = resolve(skillDir, "SKILL.md");
const packagePath = resolve(repoRoot, "dist/context-packet.skill");
const referenceUrl =
    "https://colinsalmcorner.com/from-sprints-to-swarms-part-2-context-is-infrastructure/#the-context-packet-matters";

function parseFrontmatter(content) {
    if (!content.startsWith("---\n")) {
        throw new Error("SKILL.md must start with YAML frontmatter");
    }

    const end = content.indexOf("\n---", 4);
    if (end === -1) {
        throw new Error("SKILL.md frontmatter closing marker not found");
    }

    const frontmatter = content.slice(4, end).split("\n");
    const values = {};
    let currentKey;
    let blockLines = [];

    const flushBlock = () => {
        if (!currentKey) {
            return;
        }

        values[currentKey] = blockLines.map((line) => line.trim()).join(" ").trim();
        currentKey = undefined;
        blockLines = [];
    };

    for (const line of frontmatter) {
        const keyValue = line.match(/^([A-Za-z0-9_-]+):(?:\s*(.*))?$/);
        if (keyValue) {
            flushBlock();
            const [, key, value = ""] = keyValue;
            if (value === ">" || value === "|") {
                currentKey = key;
                blockLines = [];
            } else {
                values[key] = value.trim().replace(/^["']|["']$/g, "");
            }
            continue;
        }

        if (currentKey && line.startsWith(" ")) {
            blockLines.push(line);
        }
    }

    flushBlock();
    return values;
}

const session = await joinSession({
    tools: [
        {
            name: "context_packet_skill_info",
            description:
                "Report repository-local metadata for the context-packet skill and verify that the Copilot CLI project extension loaded.",
            parameters: {
                type: "object",
                properties: {
                    includeSkillBody: {
                        type: "boolean",
                        description: "Include the full SKILL.md body in the response.",
                        default: false,
                    },
                },
            },
            skipPermission: true,
            handler: async ({ includeSkillBody = false } = {}) => {
                const skillContent = await readFile(skillPath, "utf8");
                const frontmatter = parseFrontmatter(skillContent);

                if (frontmatter.name !== "context-packet") {
                    throw new Error(`Expected skill name "context-packet", found "${frontmatter.name}"`);
                }
                if (!frontmatter.description) {
                    throw new Error("SKILL.md frontmatter must include description");
                }

                const details = [
                    "context-packet skill extension is loaded.",
                    "",
                    `Skill path: ${relative(repoRoot, skillPath)}`,
                    `Package artifact: ${relative(repoRoot, packagePath)}`,
                    `Reference: ${referenceUrl}`,
                    `Skill name: ${frontmatter.name}`,
                    `Description length: ${frontmatter.description.length} characters`,
                ];

                if (includeSkillBody) {
                    details.push("", "SKILL.md:", skillContent);
                }

                return details.join("\n");
            },
        },
    ],
});

await session.log("context-packet extension loaded");

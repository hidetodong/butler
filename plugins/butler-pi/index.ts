/**
 * Butler Pi extension — PreToolUse gate + PostToolUse advisory for Pi coding agent.
 *
 * Intercepts `write` and `edit` tool calls and delegates to Butler's shared
 * Python rule modules (butler_gate.py / butler_advisor.py) so Pi users get the
 * same phase-discipline protection as Claude Code and Codex.
 *
 * Quick-exit when BUTLER_PATH is not set or the target is not inside a
 * Butler-deployed project — zero overhead for non-Butler work.
 */
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { execSync } from "node:child_process";
import { existsSync } from "node:fs";
import { resolve } from "node:path";

// ── helpers ────────────────────────────────────────────────────────────────

/** Tools we intercept — mirrors GATED_TOOLS in butler_gate.py. */
const GATED = new Set(["write", "edit"]);

/** Mapped to Claude Code tool names that the Python modules expect. */
const TOOL_NAME_MAP: Record<string, string> = {
  write: "Write",
  edit: "Edit",
};

/**
 * Walk up from `start` looking for a `.ai/` directory that signals a
 * Butler-deployed project root.  Returns the project root or `null`.
 */
function findProjectRoot(start: string): string | null {
  let dir = resolve(start);
  // Walk up at most 8 levels (generous — real projects rarely nest deeper).
  for (let i = 0; i < 8; i++) {
    if (existsSync(resolve(dir, ".ai"))) return dir;
    const parent = resolve(dir, "..");
    if (parent === dir) break;
    dir = parent;
  }
  return null;
}

/**
 * Build the JSON payload that the Python hook dispatchers expect on stdin
 * (same shape as Claude Code PreToolUse/PostToolUse).
 */
function buildPayload(
  toolName: string,
  filePath: string,
  cwd: string,
): string {
  return JSON.stringify({
    tool_name: toolName,
    tool_input: { file_path: filePath },
    cwd,
  });
}

// ── extension ──────────────────────────────────────────────────────────────

export default function (pi: ExtensionAPI) {
  const BUTLER_PATH = process.env.BUTLER_PATH;

  // Fastest possible exit: Butler not installed at all.
  if (!BUTLER_PATH || !existsSync(BUTLER_PATH)) return;

  const gateScript = resolve(BUTLER_PATH, "templates/hooks/butler_gate.py");
  const advisorScript = resolve(
    BUTLER_PATH,
    "templates/hooks/butler_advisor.py",
  );

  // ── PreToolUse gate ──────────────────────────────────────────────────

  pi.on("tool_call", async (event, ctx) => {
    if (!GATED.has(event.toolName)) return;

    const filePath = event.input.path ?? event.input.file_path ?? "";
    if (!filePath) return;

    const projectRoot = findProjectRoot(ctx.cwd);
    // Not inside a Butler project — transparent pass-through.
    if (!projectRoot) return;

    try {
      const payload = buildPayload(
        TOOL_NAME_MAP[event.toolName] ?? event.toolName,
        filePath,
        projectRoot, // use project root as cwd for the Python scripts
      );
      execSync(`python3 "${gateScript}"`, {
        input: payload,
        encoding: "utf-8",
        stdio: ["pipe", "pipe", "pipe"],
        timeout: 5_000,
      });
      // exit 0 → allow
    } catch (err: any) {
      // exit 2 (or any non-zero) → deny
      const stderr = err.stderr ?? "";
      return {
        block: true,
        reason: stderr.trim() || `butler-gate denied ${event.toolName}`,
      };
    }
  });

  // ── PostToolUse advisory ─────────────────────────────────────────────

  pi.on("tool_result", async (event, ctx) => {
    if (!GATED.has(event.toolName)) return;

    const filePath = event.input.path ?? event.input.file_path ?? "";
    if (!filePath) return;

    const projectRoot = findProjectRoot(ctx.cwd);
    if (!projectRoot) return;

    try {
      const payload = buildPayload(
        TOOL_NAME_MAP[event.toolName] ?? event.toolName,
        filePath,
        projectRoot,
      );
      const stdout = execSync(`python3 "${advisorScript}"`, {
        input: payload,
        encoding: "utf-8",
        stdio: ["pipe", "pipe", "pipe"],
        timeout: 5_000,
      });

      if (stdout.trim()) {
        // The advisor emitted hookSpecificOutput.additionalContext.
        // Append it to the tool result so the model sees the reminder.
        let parsed: any;
        try {
          parsed = JSON.parse(stdout);
        } catch {
          return; // unparseable output — silently drop (fail-open)
        }
        const reminder = parsed?.hookSpecificOutput?.additionalContext;
        if (reminder && typeof reminder === "string") {
          const content = Array.isArray(event.content)
            ? event.content
            : [{ type: "text", text: String(event.content ?? "") }];
          return {
            content: [
              ...content,
              { type: "text", text: `\n\n${reminder}` },
            ],
          };
        }
      }
    } catch {
      // fail-open: advisory must never break the flow.
    }
  });
}

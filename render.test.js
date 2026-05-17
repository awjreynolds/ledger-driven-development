import assert from "node:assert/strict";
import test from "node:test";

import { renderLayerKey } from "./render.js";

test("renderLayerKey normalizes CAD layer names consistently", () => {
  assert.equal(renderLayerKey("  WALLS  "), "walls");
});

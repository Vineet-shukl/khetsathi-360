import fs from 'node:fs';
import path from 'node:path';

// Safely deploy React client as secondary/investor interface at /react without overwriting main legacy UI
const distIndex = path.resolve('dist/index.html');
const targetReactIndex = path.resolve('../frontend/index_react.html');
const distAssets = path.resolve('dist/assets');
const targetAssets = path.resolve('../frontend/assets');

if (fs.existsSync(distIndex)) {
  fs.copyFileSync(distIndex, targetReactIndex);
  console.log('✓ Copied dist/index.html -> frontend/index_react.html');
}

if (fs.existsSync(distAssets)) {
  fs.cpSync(distAssets, targetAssets, { recursive: true });
  console.log('✓ Synced dist/assets -> frontend/assets');
}

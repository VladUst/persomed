# Repository Guidelines

## Project Structure & Module Organization

This `client/` directory is the React 19, TypeScript, and Vite frontend for PersoMed. `src/main.tsx` mounts the app; `src/app/` contains global styles and route configuration. UI code is grouped by responsibility: `pages/` for routes, `widgets/` for page-level blocks, `features/` for user actions, `entities/` for domain displays, and `shared/` for reusable components, helpers, constants, fonts, and SVG icons. Within a module, keep components in `ui/`, types or logic in `model/`, and public exports through `index.ts`. There is currently no test directory.

## Build, Test, and Development Commands

Run these commands from `client/`:

- `npm ci` installs the versions recorded in `package-lock.json`.
- `npm run dev` starts the Vite development server (normally `http://localhost:5173`).
- `npm run build` type-checks with `tsc -b` and creates the production bundle in `dist/`.
- `npm run preview` serves that bundle locally.
- `npm run lint` checks TypeScript and TSX with ESLint; `npm run lint:fix` applies available fixes.
- `npm run lint:scss` runs Stylelint on SCSS **and applies fixes**, so review its diff afterward.

## Coding Style & Naming Conventions

Follow `.prettierrc`: two-space indentation in TS/TSX, double quotes, semicolons, trailing commas, and an 80-character line width. SCSS uses four-space indentation per `.stylelintrc.json`. Use PascalCase for React components and their folders (for example, `IndicatorForm.tsx`), `*.module.scss` for component styles, and camelCase for helpers and route functions. Import shared code through the `@/` alias, which resolves to `src/`. Keep module imports routed through existing `index.ts` exports where practical.

## Testing Guidelines

No test runner, `npm test` script, or coverage threshold is configured. For each UI change, run `npm run build` and `npm run lint`, then check the affected route or interaction in the browser. If you introduce automated tests, add a documented runner and use colocated `*.test.ts` or `*.test.tsx` names.

## Commit & Pull Request Guidelines

Recent commits use short, imperative subjects prefixed with `feat:`, `fix:`, `refactor:`, or `docs:`; follow that pattern. In a pull request, explain the behavior changed, list the checks performed, link the relevant issue when one exists, and attach screenshots for visible UI changes. Do not commit generated `dist/` files or `node_modules/`.

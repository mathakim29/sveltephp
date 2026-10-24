# SveltePHP

[![PHP 8](https://img.shields.io/badge/PHP-8.x-777BB4?logo=php&logoColor=white)](https://www.php.net/)
[![Svelte](https://img.shields.io/badge/Svelte-5-FF3E00?logo=svelte&logoColor=white)](https://svelte.dev/)

A PHP application served by FrankenPHP with a Svelte frontend compiled by Bun.
JavaScript dependencies stay inside the container.

> **Experimental:** This project is experimental and may change without notice.

## Run

This project is tested using `nerdctl` but other container runtimes should work similarly 

```sh
nerdctl compose up --build
```

The application is available at `http://localhost:8020`. 
phpMyAdmin is available at `http://localhost:8080`.

## Frontend dependencies

Frontend dependencies are declared in `packages.txt` files. The compiler
recursively checks the frontend directory and installs each package with Bun.
The following entries are examples only; use the packages required by your
frontend:

```text
dayjs@1.11.13
blockly@12.3.1
```

Use regular package imports in Svelte files:

```js
import dayjs from 'dayjs';
```

Build-time packages are hardcoded in the Dockerfile. No host-side
`package.json` is required, and `node_modules` is stored in the
container-only `/tmp/build/node_modules` volume.

## Services

- FrankenPHP serves the PHP application and compiled Svelte assets.
- Bun compiles Svelte and optionally Tailwind CSS.
- MySQL provides the application database.
- phpMyAdmin provides database administration.

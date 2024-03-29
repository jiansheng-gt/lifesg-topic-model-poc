<!--- // This file is a copy of the original found in mol-lib-config, please make modifications there instead -->
# Code of Conduct

These are the **guidelines** that have been agreed on, please try to abide by them.<br/>
There will be many instances where our files do not conform to these standards, that is ok.<br/>
Conventions do get updated over time, so do  try follow the [boy scout rule](https://deviq.com/boy-scout-rule/#targetText=The%20Boy%20Scout%20Rule%20can,cleaner%20than%20they%20found%20it.) (Leave your code better than you found it.)

---

## Table of Contents

[Commits](#Commits)<br/>
[Folder/File Conventions](#Folder/File-Conventions)<br/>
[Documentation](#Documentation)<br/>
[Coding Conventions](#Coding-Conventions)<br/>
[Testing](#Testing)<br/>
[API Routes](#API-Routes)<br/>

---

## Commits

### Branching

- We follow [Trunk-based development](https://trunkbaseddevelopment.com) in general
- Use feature toggles rather than feature branching whenever possible
- The MASTER branch should always be in a working state (ideally)
- If you do need to branch, use branch folders
- Branch name should be in all lower kebab case
- `sprint-##/mol-##-summary-of-task` for feature branches
- `release/sprint##-v#.#.#` for releases

### Commit Message

Each commit message should look like this

``` txt
[<PREFIX>][<INITIALS>] <SUMMARY>

- <DETAILS> (Optional)
- <DETAILS> (Optional)
```

- PREFIX - To tag commit to JIRA tasks
  - `[MOL-##]` for commits with open ticket
  - `[FIX]` for fixes with no open ticket
  - `[MISC]` for the uncategorized
- INITIALS - To identify persons involved
  - All persons involved should be included, whether it be pairing or code reviewer
  - `[CH]` for solo contributor
  - `[CH|KT]` for more than 1 contributor
- SUMMARY
  - Start with a summary of what was done.
  - Don't go into too much details, make sure it is short enough to be a one-liner
- DETAILS
  - Additional bullet points are to be append with a '-' (optional)
  - Leave a new line between the summary and the details so GIT GUIs will render it properly

### Definition of done

- Appropriate level of tests written (based on developer judgement and task complexity)
- Feature toggles were created and configurations for all environments were set (if applicable)
- Peer reviewed (pair programming counts)
- Merged into master
- CI is green
- Deployed onto `dev` and `qe` environment
- `CHANGELOG.md` has been updated (if applicable)
- Desk-check'd with the BA/UX/QE
- Manual/exploratory testing was done

### Versioning / Changelog

- We are adhering to [semver](https://semver.org/) for versioning
- Record meaningful changes between versions in the `CHANGELOG.md`
  - If your changes isn't slated for a new version release yet, put it under `## x.x.x` so that it may be included in the future
  - Mark breaking changes with a `**[BREAKING]**` prefix
  - Mark potentially breaking changes with a `**[WARNING]**` prefix (e.g. deprecating something)

---

## Folder/File Conventions

- **Folder** names should be kebab-lower-cased and plural
- **File** names should be descriptive
  - Pascal-cased for single exports (e.g. Class/Interface/Namespace)
  - Kebab-lower-cased for others

``` txt
src/
  something/
    models/
      SomethingDomain.ts
    entities/
      SomethingEntity.ts
    services/
      SomethingService.ts
      SomethingRepository.ts
      something-utils.ts
    SomethingController.ts
  utils/
    shared-utils.ts
```

---

## Documentation

| File | Description |
| --- | --- |
| `README.md` | Documents what this repo is about and other details that should be targeted at users. (e.g. Other devs using this repo) </br> For services hosting API docs, this file will also be rendered as the "Intro" section alongside the API docs |
| `CONTRIBUTING.md` | Documents details that should be targeted at contributors. (e.g. Those who are maintaining or adding features to this repo) |
| `CODE_OF_CONDUCT.md` | Documents best practices and conventions. </br> The master copy resides with `mol-lib-config` library and is automatically copied to every other repo that installs it.|

For backend services, API documentation can be automatically generated from the controllers using `tsoa` </br>
TSOA generates a `OpenAPI spec` file will be embedded into a `Redoc` page alongside the `README.md` </br>
This combined `Redoc` page can then be hosted using the `KoaDocs` middleware found in `mol-lib-common`

---

## Coding Conventions

### Theming with styled-components

<https://confluence.ship.gov.sg/display/MOL/Theming+with+styled-components>

### Code

- Apply [clean code](https://github.com/ryanmcdermott/clean-code-javascript) best practices
- Use tabs instead of spaces (rendered as 2 spaces preferably)
- Naming should be verbose enough to prevent miscommunication or naming conflicts
- Write comments when
  - there are special considerations/circumstances to take note of
  - the reason for "weirdness" in the code is not immediately obvious
  - the function names or variables cannot convey their intention sufficiently
- Use comment anchors to inform others on your intentions
  - `TODO` For future plans for this section of the code
  - `FIXME` For hacks that needs to be remedied on a future date
  - Others anchors can be found [here](https://marketplace.visualstudio.com/items?itemName=ExodiusStudios.comment-anchors)

### Logging

- We are using [Structured Logging](https://stackify.com/what-is-structured-logging-and-why-developers-need-it/)
- Logs needs to be searchabe/filterable on tools like kibana and grafana
- Log at the appropriate level
  - debug: For verbose logs that may help in error tracing/debugging (e.g. announcing that a function has returned)
  - info: For high level business logic flows (e.g. receiving router requests or making API calls)
  - warn: For events that may be an error/bug (e.g. failing validations)
  - error: For events that requires our attention (e.g. failing to reach the db)
  - fatal: For events that the application cannot recover from (e.g. database migration failed)

### Date/Time

- Prefer the use of JS-Joda dates to maintain the type and intent of the data
- E.g. Use `ZonedDateTime` for a specific period in time such as content publish time
- E.g. Use `LocalDate` for birthdays

### Imports / Exports

#### Avoid circular dependencies and improve import performance, by using `index.ts` barrel files in subdirectory

- Only folders representing a domain/feature should have an `index.ts` file.
- Domain/feature `index.ts` files export all the components of the current and children folders.
- `index.ts` files should not import/export other `index.ts` files.
- `index.ts` files are the only ones where relative paths and `export *` are allowed.
- In a component/module
  - Use relative imports to single components/modules of the same domain/feature level.
  - Use absolute imports to folders containing `index.ts` files of other domain/feature levels.
- Shared modules should not import specific domain modules.

E.g. given the following folder hierarchy:

```txt
src/
  components/
    models/
      users/
        Admin.ts
        index.ts
        Manager.ts
        User.ts
      reports/
        archive/
          Expired.ts
          Deletes.ts
        index.ts
        Report.ts
    services/
      users/
        index.ts
        UserService.ts
      reports/
        index.ts
        ReportService.ts
  shared/
    index.ts
    Utils.ts
```

- `components/`, `components/models/`, and `services/` folders don't have an `index.ts` file because there are too high level folders and don't represent a domain/feature.
- `components/models/reports/archive/` folder doesn't have an `index.ts` file because it is part of the reports domain/feature. `archive/` components are exported in `reports/index.ts` file.
- `Utils.ts` can not import any modules `from components/`.
- `services/reports/index.ts` file exports `ReportService.ts` this way: `export * from "./ReportService";`
- `services/reports/index.ts` file exports `archive/Expired.ts` this way: `export * from "./archive/Expired.ts";`
- `ReportService.ts` imports `Report.ts` and `Expired.ts` this way: `import { Expired, Report } from "src/components/models/reports";`
- `Admin.ts` imports `Utils.ts` this way: `import { Utils } from "src/shared";`

#### Make imports/exports less confusing and easier to find references in codebase by

- Not using export default

```js
// Nope!
export default () => { };
// Yay!
export const MyComponent = () => { };
```

- Avoiding renaming imports

```js
// Nope!
import { MyComponent as comp } from "src/components";
// Yay!
import { MyComponent } from "src/components";
```

- Exporting near the top-level. Limit nesting.

```js
// Nope!
export const BigComponent {
  myConst: "value";
  myHelperFunc: () => { };
  MyComponent: () => { };
};
// Yay!
export const myConst = "value";
export function myHelperFunc() { };
export const MyComponent = () => { };
```

- Explicitly listing imported names

```js
// Nope!
import MyComponent from "src/components";
import myHelperFunc from "src/components";
import myConst from "src/components";
// Yay!
import { MyComponent, myHelperFunc, myConst } from "src/components";
```

- No star import. Even if it creates more line of code, keep listing imported names.

```js
// Nope!
import * as components from "src/components";
// Yay!
import { MyComponent, myHelperFunc, myConst } from "src/components";
```

- No Re-export. Unless you want to extend a module, but such case should not happen.

```js
// Nope!
export { TheOldComponent as MyComponent } from "src/components";
export * as TheOldComponent from "src/components";` Nope!
```

- No Namespace. Provides very little value when working with modules.

#### If you'd like to read more about it

- [Circular dependencies](https://medium.com/visual-development/how-to-fix-nasty-circular-dependency-issues-once-and-for-all-in-javascript-typescript-a04c987cf0de)
- [Modules in TypeScript](https://www.typescriptlang.org/docs/handbook/modules.html)

---

## Testing

- Targeted tests (e.g. Unit/Integration/Benchmark/External) should be placed in the `__tests__` folder at the lowest-common-directory level of what's being tested
- Broader tests (e.g. Functional/Load) should be placed at the project root's `__tests__` folder
- Tests that don't allow network/dependencies should have their dependencies mocked (e.g. database, agency APIs, message queues)
- Consider using `nock` if you only need to mock API responses in an automated test (e.g. jest), but create a `/mock` controller if it's required in manual/UI testing
- Complex tests are more costly to write and maintain, consider using the "lowest level" test possible to meet your testing goals
- Reference project in `mol-auth-forwarder`

``` txt
__tests__/
  functional/
    functional-test.spec.ts
  load/
    load-test.spec.ts

src/
  __tests__/
    super-test.super.spec.ts
    component-1-and-2-test.spec.ts
  folder-1/
    component-1.ts
    component-1-unit-test.spec.ts
    component-1-benchmark-test.bench.spec.ts
    component-1-external-integration-test.ext.spec.ts
  folder-2/
    component-2.ts
```

| Legends | Description |
| --- | --- |
| `CI` | Whether these tests should be automatically ran on the CI pipeline |
| `Network/Deps` | Whether these tests are allowed to access external services (e.g. database, agency APIs, message queues) |
| `Setup` | Whether these tests are allowed to have an environmental setup/seeding stage |
</br>

| Test | Purpose | CI | Network/Deps | Setup | File Pattern | NPM Command |
| --- | --- | :---: | :---: | :---: | --- | --- |
| `Unit` | Testing a function/feature | ✓ | ✗ | ✗ | `<root>/src/**/__tests__/<name>.spec.ts` | test |
| `API Integraton` | Testing the service on the API level using [supertest](https://github.com/visionmedia/supertest) | ✓ | ✗ | ✗ | `<root>/src/__tests__/<name>.super.spec.ts` | test |
| `External Integration` | Testing our integration against external services/dependencies</br>(e.g. DB, agency API endpoints, another microservice) | ✗ | ✓ | ✓ | `<root>/src/**/__tests__/<name>.ext.spec.ts` | test:ext |
| `Benchmark` | Testing optimization impact (or lack thereof) | ✗ | ✓ | ✓ | `<root>/src/**/__tests__/<name>.bench.spec.ts` | test:bench |
| `Functional` | Testing API/Mobile automation against a full env (e.g. E2E) | ✓ | ✓ | ✓ | `<root>/__tests__/functional/**/<name>.spec.ts` | test:func -- \<env\> |
| `Load` | Testing API automation against a full env (e.g. E2E) to ensure that it can handle an expected load using [k6](https://k6.io/blog/comparing-best-open-source-load-testing-tools) | ✓ | ✓ | ✓ | `<root>/__tests__/load/**/<name>.spec.ts` | test:load -- \<env\> |

---

## API Routes

- API routes should begin with `${DOMAIN}/api/`
- Health check routes should begin with `${DOMAIN}/health/`
- Mock routes should begin with `${DOMAIN}/mock/`
- Document routes should begin with `${DOMAIN}/docs/`
- More details [here](https://confluence.ship.gov.sg/display/MOL/Web+API+Design+Guidelines)

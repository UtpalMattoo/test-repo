# Dog Shelter - Frontend

Astro + Svelte frontend for the Tailspin Dog Shelter adoption application.

## New Components

### AdoptionForm.svelte

Interactive form component for submitting dog adoption applications.

**Props:**
- `dogId: number` - ID of the dog to apply for
- `hasApplication: boolean` - Whether the dog already has an application

**Features:**
- Real-time client-side validation (name, email, phone)
- Loading states during submission
- Success/error message display
- Dark mode styling with terminal-inspired design
- Accessibility support with ARIA labels and test IDs

**Validation Rules:**
- Name: 2-50 characters required
- Email: Valid format required (user@domain.com)
- Phone: US format required (555) 123-4567, 555-123-4567, or 5551234567

**Usage:**
```svelte
<AdoptionForm dogId={1} hasApplication={false} />
```

### DogDetails.svelte (Updated)

Enhanced dog detail component that now includes the adoption form for available dogs.

**New Features:**
- Integrates AdoptionForm component for available dogs
- Displays adoption form only when dog status is 'AVAILABLE'
- Shows "has application" message when dog already has an application
- Passes dog ID and application status to form component

**Props:** (unchanged)
- `dog: Dog | undefined` - Dog object to display
- `dogId: number` - ID of dog to fetch and display

## 🚀 Project Structure

Inside of your Astro project, you'll see the following folders and files:

```text
/
├── public/
│   └── favicon.svg
├── src/
│   ├── layouts/
│   │   └── Layout.astro
│   └── pages/
│       └── index.astro
└── package.json
```

To learn more about the folder structure of an Astro project, refer to [our guide on project structure](https://docs.astro.build/en/basics/project-structure/).

## 🧞 Commands

All commands are run from the root of the project, from a terminal:

| Command                   | Action                                           |
| :------------------------ | :----------------------------------------------- |
| `npm install`             | Installs dependencies                            |
| `npm run dev`             | Starts local dev server at `localhost:4321`      |
| `npm run build`           | Build your production site to `./dist/`          |
| `npm run preview`         | Preview your build locally, before deploying     |
| `npm run astro ...`       | Run CLI commands like `astro add`, `astro check` |
| `npm run astro -- --help` | Get help using the Astro CLI                     |

## 👀 Want to learn more?

Feel free to check [our documentation](https://docs.astro.build) or jump into our [Discord server](https://astro.build/chat).

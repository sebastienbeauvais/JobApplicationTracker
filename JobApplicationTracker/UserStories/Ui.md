# Title
Create a clean UI for the application

# Description
As a user, I want clean and modern UI with consitent feel across the application. It should feel like an apple application. A dark mode should be available.

# Acceptance Criteria
- Clean UI reminicent of app products/applications
- Dark mode available via a toggle. State of Dark/Light mode should be consistent even after exiting the application

# Logic

## Design Aesthetic
- **Apple website inspired** - Clean, minimal, spacious
- Generous whitespace
- Subtle shadows and rounded corners
- Smooth transitions and animations
- Focus on typography and readability

## Color Scheme
- **Neutral palette** with Material Design influences
- Light mode: White/light gray backgrounds, dark text
- Dark mode: Dark gray/black backgrounds, light text
- Accent color: Neutral blue (can be refined later)

## Dark Mode
- Toggle switch in navigation/header area
- **State persists** across browser sessions (stored in localStorage)
- Smooth transition between modes
- All components must support both modes

## Layout & Navigation
- Clean header with navigation links
- Responsive design (mobile-friendly)
- Consistent spacing and alignment across all pages

## Pages
| Route | Purpose |
|-------|---------|
| `/` | Dashboard (homepage) with metrics |
| `/add-job` | Add new job application form |
| `/jobs` | List all applications with inline editing |

## Inline Editing (Jobs List)
- Edit fields directly in the table/list view
- Editable fields: Status, Got Interview, Coding Question Link
- Save on change (auto-save) or explicit save button (TBD based on feel)
- Visual feedback on successful save

## Components
- Consistent button styles (primary, secondary)
- Form inputs with clear labels and validation states
- Status badges with color coding
- Toggle switches for boolean fields
- Dropdown selects for status
- Data tables with clean styling

## No Delete Functionality
- Users cannot delete job applications at this time
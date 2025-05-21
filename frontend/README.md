# Voice Generation Frontend

A modern React frontend for the Nari Labs voice generation service. Built with React, TypeScript, Tailwind CSS, and shadcn/ui components.

## Features

- Clean and intuitive user interface
- Text input for voice generation
- Emotion selection (happy, sad, angry, neutral, excited)
- Tone selection (formal, casual, professional, friendly)
- Pace control with a slider
- Real-time audio playback
- Responsive design

## Getting Started

### Prerequisites

- Node.js 16.x or later
- npm 7.x or later

### Installation

1. Clone the repository
2. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
3. Install dependencies:
   ```bash
   npm install
   ```

### Development

To start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:5173`.

### Building for Production

To create a production build:

```bash
npm run build
```

The built files will be in the `dist` directory.

### Preview Production Build

To preview the production build locally:

```bash
npm run preview
```

## Configuration

The frontend is configured to connect to the voice generation API at `https://<pod>.runpod.net`. Update the API URL in `src/App.tsx` to point to your deployment.

## Technologies Used

- React 18
- TypeScript
- Tailwind CSS
- shadcn/ui
- Vite
- Radix UI 
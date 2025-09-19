# Setup Guide

This guide provides instructions on how to set up and run the AI-powered farming assistant application for local development and how to deploy it to Vercel.

## Vercel Deployment

This project is structured to be deployed on Vercel with the Next.js frontend and the Python backend as a Serverless Function.

1.  **Connect your Git repository to Vercel.**
2.  **Configure Environment Variables in Vercel:**
    In your Vercel project settings, add the following environment variable:

    *   `HF_TOKEN`: Your Hugging Face token. The AI agent needs this to download the model.

    You do **not** need to set `NEXT_PUBLIC_BACKEND_URL` for the Vercel deployment. The frontend will automatically use the relative path `/api/predict` to communicate with the backend.

3.  **Deploy.** Vercel will automatically use the `vercel.json` file to build and deploy both the Next.js frontend and the Python API.

## Local Development Setup

For local development, you need to run the frontend and backend servers separately.

### Backend Setup (Disease Detection Agent)

The backend is a Python FastAPI application located in the `api` directory.

#### 1. Prerequisites

*   Python 3.8 or higher
*   pip (Python package installer)

#### 2. Installation

1.  From the root of the project, install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

#### 3. Environment Variable

1.  The backend needs your Hugging Face token. Set it as an environment variable in your shell:

    ```bash
    export HF_TOKEN="<your_hugging_face_token>"
    ```

#### 4. Running the Backend

1.  From the root directory of the project, run the following command to start the backend server:

    ```bash
    uvicorn api.main:app --reload --port 8000
    ```

2.  The server will start on `http://localhost:8000`. The prediction endpoint will be at `http://localhost:8000/api/predict`.

### Frontend Setup

The frontend is a Next.js application.

#### 1. Prerequisites

*   Node.js 18 or higher
*   pnpm (or npm/yarn)

#### 2. Installation

1.  Install the dependencies using `pnpm`:

    ```bash
    pnpm install
    ```

#### 3. Environment Variable

1.  To connect the local frontend to the local backend, create a new file named `.env.local` in the root of the project.
2.  Add the following line to the `.env.local` file, which should be the full URL to the local backend's prediction endpoint:

    ```
    NEXT_PUBLIC_BACKEND_URL=http://localhost:8000/api/predict
    ```

#### 4. Running the Frontend

1.  To run the frontend in development mode, use the following command:

    ```bash
    pnpm dev
    ```

2.  The application will be available at `http://localhost:3000`.

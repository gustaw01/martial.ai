import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'

const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:3000';

export const apiSlice = createApi({
    baseQuery: fetchBaseQuery({ baseUrl: apiUrl }),
    tagTypes: ['History', 'PlagiarismAssessment'],
    endpoints: (builder) => ({}),
})
import { createSelector, createEntityAdapter } from "@reduxjs/toolkit";
import { apiSlice } from "../../app/api/apiSlice";

// Konfiguracja adaptera
const historiesAdapter = createEntityAdapter();

// Stan początkowy dla adaptera
const initialState = historiesAdapter.getInitialState();

export const historiesApiSlice = apiSlice.injectEndpoints({
    endpoints: (builder) => ({
        getHistories: builder.query({
            query: () => '/history',
            transformResponse: (responseData) => 
                historiesAdapter.setAll(initialState, responseData),
            providesTags: (result, error, arg) =>
                result
                    ? [
                        { type: 'History', id: "LIST" },
                        ...result.ids.map((id) => ({ type: 'History', id })),
                      ]
                    : [{ type: 'History', id: "LIST" }],
        }),
        addNewHistory: builder.mutation({
            query: (newHistory) => ({
                url: '/history',
                method: 'POST',
                body: newHistory,
            }),
            invalidatesTags: [{ type: 'History', id: "LIST" }],
        }),
        updateHistory: builder.mutation({
            query: (updatedHistory) => ({
                url: `/history/${updatedHistory.id}`,
                method: 'PUT',
                body: updatedHistory,
            }),
            invalidatesTags: (result, error, { id }) => [{ type: 'History', id }],
        }),
        uploadHistoryPDF: builder.mutation({
            query: ({ id, file }) => {
                const formData = new FormData();
                formData.append('file', file);
                return {
                    url: `/history/pdf`,
                    method: 'POST',
                    body: formData,
                };
            },
            invalidatesTags: (result, error, { id }) => [{ type: 'History', id }],
        }),
        uploadHistoryDOCX: builder.mutation({
            query: ({ id, file }) => {
                const formData = new FormData();
                formData.append('file', file);
                return {
                    url: `/history/docx`,
                    method: 'POST',
                    body: formData,
                };
            },
            invalidatesTags: (result, error, { id }) => [{ type: 'History', id }],
        }),
        deleteHistory: builder.mutation({
            query: ({ id }) => ({
                url: `/history/${id}`,
                method: 'DELETE',
            }),
            invalidatesTags: (result, error, { id }) => [{ type: 'History', id }],
        }),
    }),
});

export const {
    useGetHistoriesQuery,
    useAddNewHistoryMutation,
    useUpdateHistoryMutation,
    useUploadHistoryPDFMutation,
    useUploadHistoryDOCXMutation,
    useDeleteHistoryMutation,
} = historiesApiSlice;

// Zwraca wynik zapytania
export const selectHistoriesResult = historiesApiSlice.endpoints.getHistories.select();

// Tworzy memoizowany selektor
const selectHistoriesData = createSelector(
    selectHistoriesResult,
    (historiesResult) => historiesResult?.data ?? initialState // Obsługa braku danych
);

// Generuje selektory z adaptera i mapuje nazwy
export const {
    selectAll: selectAllHistories,
    selectById: selectHistoryById,
    selectIds: selectHistoryIds,
} = historiesAdapter.getSelectors(
    (state) => selectHistoriesData(state)
);